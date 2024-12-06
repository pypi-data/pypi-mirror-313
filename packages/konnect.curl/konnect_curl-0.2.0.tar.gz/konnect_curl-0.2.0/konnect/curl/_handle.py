# Copyright 2023-2024  Dom Sekotill <dom.sekotill@kodo.org.uk>

import pycurl


class Handle:
	"""
	A proxy to a Curl handle for concrete `Request` class implementers' use
	"""

	def __init__(self, handle: pycurl.Curl) -> None:
		self._handle = handle

	def setopt(self, option: int, value: object, /) -> None:
		self._handle.setopt(option, value)

	def unsetopt(self, option: int, /) -> None:
		self._handle.unsetopt(option)

	def getinfo(self, option: int, /) -> object:
		return self._handle.getinfo(option)  # type: ignore [no-untyped-call]

	def getinfo_raw(self, option: int, /) -> object:
		return self._handle.getinfo_raw(option)  # type: ignore [no-untyped-call]

	def pause(self, state: int, /) -> None:
		self._handle.pause(state)  # type: ignore [no-untyped-call]
