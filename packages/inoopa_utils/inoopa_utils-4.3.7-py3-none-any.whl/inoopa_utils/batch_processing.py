# For local dev purpose only
from dotenv import load_dotenv

load_dotenv()
import json
import time
import traceback
from typing import Callable
from requests import Session
from functools import partial
from queue import Queue, Empty
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor

from inoopa_utils.inoopa_logging import create_logger
from inoopa_utils.mongodb_helpers import DbManagerMongo
from inoopa_utils.rabbitmq_helpers import get_messages_from_queue, push_to_queue


def parralelize_company_processing_and_saving(
    processing_function: Callable,
    input_queue_name: str,
    process_name: str,
    processing_function_need_session: bool = False,
    pretty_logging: bool = False,
) -> None:
    """
    Process the queue of companies to process and save them in DB.
    It can seems overengineered but we went from 20 days to 2h to scrape the whole BCE database with this.

    In this function, 2 groups of threads are running in parallel:
        - Multiple threads for processing
        - 1 thread for saving in DB

    :param processing_function: function to use to process the companies. Any function used here should these params:
        - `params` as a parameter. This is the dict containing the company params to process. This can be nammed as you want.
        - `queue_name` as a parameter. This is the name of the queue to push the companies to requeue
            or to deduce the dead letter queue name in case of erroers.
        - Optional: `session` as a parameter. This is only needed if the processing function makes a lot of requests.
    :param input_queue_name: name of the queue containing the companies to process with it's params
    :param process_name: name of the process function (for logging purpose) ex: bce_scraper, website_finder,...
    :param processing_function_need_session: whether the processing function needs a session or not.
        When the processing function makes a lot of requests, it is better to use a session
        to avoid creating a new connection for each request. (your function should have a `session` as a parameter)
    """
    logger = create_logger(f"INOOPA.ETL.{process_name.upper()}.BATCH_PROCESSING", pretty=pretty_logging)
    dead_letter_queue_name = f"{input_queue_name}_DLQ"
    # This queue is processed in a separate thread to avoid blocking the main thread (processing) when saving in DB
    db_queue = Queue()
    # This event will be used to send an exit signal to the DB thread
    db_thread_exit_signal = Event()
    # This thread will consume the db_queue and save companies in DB in a separate thread
    # This is done to avoid blocking the main thread (scraping) when saving in DB (which can take a while)
    db_manager_thread = Thread(target=_save_companies_in_db, args=(db_queue, db_thread_exit_signal), daemon=True)
    db_manager_thread.start()

    while True:
        # This queue's messages should only contains a list of companies number
        queue_message = get_messages_from_queue(input_queue_name)
        if not queue_message:
            logger.info("No more companies to process, stop...")
            # Send the exit signal to the DB thread
            db_thread_exit_signal.set()
            break

        try:
            # This will load a list of dict from the queue message. Each dict represent one company to process.
            # This dict should contains the keys the processing function needs.
            # The bce_scraper only needs the company number for example.
            # So the queue messages should contain a LIST of DICT like this: [{"company_number": "0649.973.640"},...]
            processing_function_params = json.loads(queue_message[0])
            logger.info(f"Processing {len(processing_function_params)} companies...")
            if processing_function_need_session:
                with Session() as session:
                    with ThreadPoolExecutor() as executor:
                        processed_companies = list(
                            executor.map(
                                partial(processing_function, queue_name=input_queue_name, session=session),
                                processing_function_params,
                            )
                        )
            else:
                with ThreadPoolExecutor() as executor:
                    processed_companies = list(
                        executor.map(
                            partial(processing_function, queue_name=input_queue_name),
                            processing_function_params,
                        )
                    )
            # Add companies to the python queue to be saved in DB
            if processed_companies:
                db_queue.put(processed_companies)
        except Exception as ex:
            logger.error(
                f"Error: {ex} while processing batch, sending batch to dead-letter-queue: {dead_letter_queue_name}"
            )
            # print traceback in case of error for debugging purpose
            traceback.print_exc()
            push_to_queue(dead_letter_queue_name, processing_function_params)
            # Send the exit signal to the DB thread
            db_thread_exit_signal.set()
            # Wait for the DB thread to finish before exiting (Wait for all the companies to be saved in DB)
            db_manager_thread.join()
            raise ex
    # Wait for the DB thread to finish before exiting (Wait for all the companies to be saved in DB)
    db_manager_thread.join()


def _save_companies_in_db(db_python_queue: Queue, exit_signal: Event) -> None:
    """
    Save companies in DB.

    :param db_python_queue: queue containing the companies to save in DB
    :param exit_signal: event to send an exit signal to the thread
    """
    _logger = create_logger("INOOPA.BATCH_PROCESSING.DB_THREAD")
    db_manager = DbManagerMongo()
    # Wait for the python queue to be empty and the exit signal to be set to end the thread
    while True:
        try:
            # A batch of companies is pulled from the python queue.
            # Pull during 1 second max to avoid blocking the thread. DO NOT REMOVE THE TIMEOUT!
            companies = db_python_queue.get(timeout=1)
            db_manager.update_or_add_many_to_collection(companies)
        except Empty:
            if exit_signal.is_set():
                break
            time.sleep(1)
    _logger.info("DB thread exiting...")
