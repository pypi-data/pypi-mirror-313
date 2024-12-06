#####################################################################################
# A package to simplify the creation of Python Command-Line tools
# Copyright (C) 2023  Benjamin Davis
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; If not, see <https://www.gnu.org/licenses/>.
#####################################################################################

from __future__ import annotations
from typing import Any, Callable, Mapping, TypeVar, Type, ClassVar, NoReturn

import sys
from dataclasses import Field, dataclass, MISSING, fields
from enum import Enum
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
import re

#####################################################################################
# Version Information
#####################################################################################
from command_creator._info import __version__

version_info = [int(x) if x.isdigit() else x for x in re.split(r"\.|-", __version__)]


#####################################################################################
# Error Information
#####################################################################################
class InvalidArgumentError(Exception):
  """Error raised when an invalid argument is passed to a command
  """
  pass


#####################################################################################
# Useful Constants
#####################################################################################
SUCCESS = 0
FAILURE = 1


#####################################################################################
# Command Argument
#####################################################################################
class CmdArgument(Field):
  """Class which represents a command-line argument
  """
  __slots__ = ("help", "abrv", "choices", "optional")

  def __init__(
        self,
        help: str = "",
        abrv: str | None = None,
        choices: list[str] | type[Enum] | None = None,
        optional: bool = False,
        default: Any = MISSING,
        default_factory: Callable[[], Any] = lambda: MISSING,
        init: bool = True,
        repr: bool = True,
        hash: bool | None = None,
        compare: bool = True,
        metadata: Mapping[Any, Any] = dict(),
        **kwargs: Any
      ) -> None:
    if (sys.version_info >= (3, 10)):
      if "kw_only" not in kwargs:
        kwargs["kw_only"] = False

    super().__init__(default, default_factory, init, repr, hash, compare, metadata, **kwargs)

    if default_factory() is MISSING:
      self.default_factory = MISSING

    self.help = help
    self.abrv = abrv
    self.choices = choices
    self.optional = optional


def arg(
      help: str = "",
      abrv: str | None = None,
      choices: list[str] | type[Enum] | None = None,
      optional: bool = False,
      default: Any = MISSING,
      default_factory: Callable[[], Any] = lambda: MISSING,
      init: bool = True,
      repr: bool = True,
      hash: bool | None = None,
      compare: bool = True,
      metadata: Mapping[Any, Any] = dict(),
      **kwargs: Any
    ) -> Any:
  """Create a command-line argument

  Args:
      help (str, optional): Help message for the argument. Defaults to empty string.
      abrv (str | None, optional): Abbreviation for the argument. Defaults to None.
      choices (list[str] | Enum | None, optional): List of choices for the argument.
        Defaults to None.
      optional (bool, optional): Whether the argument is optional. Defaults to False.
      default (Any, optional): Default value for the argument. Defaults to MISSING.
      default_factory (Callable[[], Any], optional): Default factory for the argument.
        Defaults to lambda: MISSING.
      init (bool, optional): Whether the argument is included in the __init__ method.
        Defaults to True.
      repr (bool, optional): Whether the argument is included in the __repr__ method.
        Defaults to True.
      hash (bool | None, optional): Whether the argument is included in the __hash__ method.
        Defaults to None.
      compare (bool, optional): Whether the argument is included in the __eq__ method.
        Defaults to True.
      metadata (Mapping[Any, Any], optional): Metadata for the argument. Defaults to dict().
      **kwargs (Any): Additional keyword arguments for the argument.

  Returns:
      Any: The command-line argument
  """
  if sys.version_info >= (3, 10):
    if "kw_only" not in kwargs:
      kwargs["kw_only"] = False

  return CmdArgument(
    help=help,
    abrv=abrv,
    choices=choices,
    optional=optional,
    default=default,
    default_factory=default_factory,
    init=init,
    repr=repr,
    hash=hash,
    compare=compare,
    metadata=metadata,
    **kwargs
  )


#####################################################################################
# Command Class
#####################################################################################
@dataclass
class Command(ABC):
  """Class which represents a command-line command
  """

  sub_commands: ClassVar[dict[str, Type[Command]]] = dict()
  sub_command: Command | None

  @abstractmethod
  def __post_init__(self) -> None:
    """This method must be implemented by subclasses in order to setup variables or
    post-process any user inputs
    """
    pass

  @abstractmethod
  def __call__(self) -> int:
    """This method must be implemented by subclasses, it is the method which is called
    to execute the command
    """
    pass

  @classmethod
  def create_parser(cls: Type[CommandT]) -> ArgumentParser:
    parser = ArgumentParser(
      prog=cls.__name__.lower(),
      description=cls.__doc__,
    )
    cls._add_args(parser)
    cls._add_sub_commands(parser)
    return parser

  @classmethod
  def _add_args(cls, parser: ArgumentParser) -> None:
    """Add arguments to the parser

    Args:
        parser (ArgumentParser): The parser to add arguments to
    """
    for fld in fields(cls):
      if "ClassVar" in str(fld.type):
        continue
      if fld.name == "sub_command":
        continue
      if not isinstance(fld, CmdArgument):
        raise InvalidArgumentError(
          f"Field {fld.name} is not a CmdArgument" +
          " Did you use field() instead of arg()?"
        )

      kwargs: dict[str, Any] = dict()

      if 'list' in fld.type:
        kwargs['nargs'] = '+'
      elif 'bool' in fld.type:
        if fld.default is MISSING or fld.default is False:
          kwargs['action'] = 'store_true'
          kwargs['default'] = False
        else:
          kwargs['action'] = 'store_false'
          kwargs['default'] = True
      elif 'str' in fld.type:
        kwargs['type'] = str
      elif 'str' in fld.type:
        kwargs['type'] = int
      elif 'int' in fld.type:
        kwargs['type'] = int
      elif 'float' in fld.type:
        kwargs['type'] = float

      if fld.optional:
        if 'nargs' not in kwargs:
          kwargs['nargs'] = '?'
        else:
          kwargs['nargs'] = '*'

      if fld.choices is not None:
        if isinstance(fld.choices, list):
          kwargs['choices'] = fld.choices
        elif issubclass(fld.choices, Enum):
          kwargs['choices'] = [str(e).replace(fld.choices.__name__ + ".", "") for e in fld.choices]
        else:
          raise ValueError(
            f"Field {fld.name} has an invalid type for choices" +
            " Did you use an Enum or a list?"
          )

      if fld.default is not MISSING:
        kwargs['default'] = fld.default

      kwargs['help'] = fld.help

      if fld.default is MISSING and fld.default_factory is MISSING:
        parser.add_argument(fld.name, **kwargs)
      elif fld.abrv is not None:
        parser.add_argument(f"--{fld.name}", f"-{fld.abrv}", **kwargs)
      else:
        parser.add_argument(f"--{fld.name}", **kwargs)

  @classmethod
  def _add_sub_commands(cls, parser: ArgumentParser) -> None:
    """Add sub-commands to the parser

    Args:
        parser (ArgumentParser): The parser to add sub-commands to
    """
    if len(cls.sub_commands) == 0:
      return

    sub_parsers = parser.add_subparsers(dest="sub_command", required=False)

    for sub_cmd_name, sub_cmd in cls.sub_commands.items():
      sub_parser = sub_parsers.add_parser(
        sub_cmd_name,
        usage=sub_cmd.__doc__,
      )
      sub_cmd._add_args(sub_parser)
      sub_cmd._add_sub_commands(sub_parser)

  @classmethod
  def from_args(cls: Type[CommandT], args: Namespace) -> CommandT:
    """Create a command from a list of arguments

    Args:
        args (list[str]): The arguments to create the command from

    Returns:
        CommandT: The created command
    """
    arg_dict = {}

    for fld in fields(cls):
      if not isinstance(fld, CmdArgument):
        if fld.name == "sub_command":
          continue
        raise InvalidArgumentError(
          f"Field {fld.name} is not a CmdArgument" +
          " Did you use field() instead of arg()?"
        )

      arg_dict[fld.name] = getattr(args, fld.name)

      if 'list' in fld.type and fld.optional:
        if arg_dict[fld.name] is None:
          arg_dict[fld.name] = []
        elif len(arg_dict[fld.name]) == 0:
          arg_dict[fld.name] = None

    if len(cls.sub_commands) != 0 and args.sub_command is not None:
      arg_dict["sub_command"] = cls.sub_commands[args.sub_command].from_args(args)
    else:
      arg_dict["sub_command"] = None

    return cls(**arg_dict)

  @classmethod
  def execute(cls: Type[CommandT]) -> NoReturn:
    """Execute the command and exit with the return code
    """
    parser = cls.create_parser()
    args = parser.parse_args()
    cmd = cls.from_args(args)
    exit(cmd())

  @classmethod
  def auto_complete(cls: Type[CommandT]) -> None:
    """Print the auto-complete options for the command
    """
    # Check if we are in a sub-command
    for sub_cmd_name, sub_cmd in cls.sub_commands.items():
      if sub_cmd_name in sys.argv:
        sub_cmd.auto_complete()
        return

    # Check if we are in a choice
    last_flag = None
    last_choice = None
    for arg_name in reversed(sys.argv):
      if arg_name == sys.argv[0]:
        break
      if arg_name.startswith("-"):
        last_flag = arg_name
        break
      else:
        last_choice = arg_name

    if last_flag is not None:
      last_flag = last_flag.replace("-", "")

      for fld in fields(cls):
        if not isinstance(fld, CmdArgument):
          if fld.name == "sub_command":
            continue
          raise InvalidArgumentError(
            f"Field {fld.name} is not a CmdArgument" +
            " Did you use field() instead of arg()?"
          )
        if fld.name == last_flag or fld.abrv == last_flag:
          if fld.choices is not None:
            if last_choice is not None and last_choice in fld.choices:
              if 'list' in fld.type:
                for choice in fld.choices:
                  print(choice)
                break

            for choice in fld.choices:
              print(choice)
            return

    # Otherwise print the options
    for sub_cmd_name in cls.sub_commands.keys():
      print(sub_cmd_name)

    for fld in fields(cls):
      if not isinstance(fld, CmdArgument):
        if fld.name == "sub_command":
          continue
        raise InvalidArgumentError(
          f"Field {fld.name} is not a CmdArgument" +
          " Did you use field() instead of arg()?"
        )

      if fld.default is MISSING and fld.default_factory is MISSING:
        if fld.choices is not None:
          for choice in fld.choices:
            print(choice)
      else:
        print(f"--{fld.name}")
        if fld.abrv is not None:
          print(f"-{fld.abrv}")


#####################################################################################
# Type Information
#####################################################################################
CommandT = TypeVar("CommandT", bound="Command")
