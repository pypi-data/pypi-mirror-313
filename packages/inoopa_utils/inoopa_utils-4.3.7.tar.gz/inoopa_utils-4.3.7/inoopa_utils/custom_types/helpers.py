# class EasyEnum(str):
#     """
#     Enum like class that you can use without the anying .value

#     Usage:
#     ```python
#     class RegionBe(EasyEnum):
#         wallonia = "Wallonia"
#         flamande = "Flamande"
#         bruxelles = "Bruxelles"

#     RegionBe('wallonia')     # returns Wallonia
#     RegionBe.wallonia        # returns Wallonia
#     RegionBe.get_all_values  # returns ['Wallonia', 'Flamande', 'Bruxelles']
#     RegionBe('bad value')    # returns 'NOT FOUND'
#     ```
#     """

#     _not_found = "NOT FOUND"

#     def __new__(cls, value, *args, **kwargs):
#         obj = str.__new__(cls, value)
#         obj._value_ = value  # type: ignore
#         return obj

#     def __str__(self):
#         return str(self.value)

#     def __repr__(self):
#         return str(self.value)

#     @classmethod
#     def get_all_values(cls) -> list[str]:
#         return [v for k, v in cls.__dict__.items() if not k.startswith("_") and isinstance(v, str)]

#     @classmethod
#     def _missing_(cls, value):
#         for k, v in cls.__dict__.items():
#             if isinstance(v, str) and v.lower() == str(value).lower():
#                 return v
#         return cls._not_found

#     @classmethod
#     def __getattr__(cls, name):
#         try:
#             return cls.__dict__[name]
#         except KeyError:
#             return cls._not_found

#     @classmethod
#     def __call__(cls, value):
#         return cls._missing_(value)

#     @classmethod
#     def __contains__(cls, value):
#         return value in cls.get_all_values()

from enum import Enum, unique


# Example usage:
class RegionBe(Enum):
    wallonia = "Wallonia"
    flamande = "Flamande"
    bruxelles = "Bruxelles"
    not_found = "NOT FOUND"

    @classmethod
    def get_all_values(cls) -> list[str]:
        return [v.value for v in cls.__dict__.values() if isinstance(v, RegionBe)]


print(RegionBe.get_all_values())
print(RegionBe.wallonia.value)
print(RegionBe("Wallonia").value)
