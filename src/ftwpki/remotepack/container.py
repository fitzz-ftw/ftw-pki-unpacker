# File: src/ftwpki/remotepack/container.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
container
===============================

This module provides container classes for handling remote cryptographic keys and certificates.

"""

import sys
import tomllib
from io import BytesIO
from pathlib import Path
from typing import Any, Literal
from zipfile import ZIP_DEFLATED, ZipFile

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat
from cryptography.x509.base import Certificate

from ftwpki.baselibs.exceptions import PKIMissingExportPathError
from ftwpki.baselibs.transport import validate_and_format_chain


class RemoteKeys:
    """
    Base class for storing remote cryptographic components.
    """
    __slots__ = ["_fullchain", "_rootca", "_private_key"]
    
    def __init_subclass__(cls) -> None:
        """
        Set up the slots for subclasses based on the parent class.
        """
        cls.__slots__ = RemoteKeys.__slots__

    def keys(self) -> list[str]:
        """
        Get the names of the stored cryptographic components.

        :returns: A list of keys representing the stored components.
        """
        return [e.lstrip("_") for e in self.__slots__]

    def items(self) -> list[tuple[str, Any]]:
        """
        Get the stored components as key-value pairs.

        :returns: A list of tuples containing component names and their values.
        """
        keys = self.keys()
        return [(k, self[f"{k}"]) for k in keys]

    def __getitem__(self, key:str)->Any:
        """
        Get a specific cryptographic component by its key.

        :param key: The name of the component to retrieve.
        :raises KeyError: If the requested key does not exist.
        :returns: The value of the requested cryptographic component.
        """
        try:
            return getattr(self, f"_{key}")
        except AttributeError as e:
            raise KeyError(e)

    def __repr__(self) -> str:
        repr=[]
        for k, v in zip(self.keys(), self.__slots__, strict=True):
            vstr = getattr(self, v, "unknown")
            repr.append(f"\n  {k}: {vstr}")
        return f"{self.__class__.__name__}({', '.join(repr)}\n)"


class RemotePathes(RemoteKeys):
    """
    Class to store the file paths of remote cryptographic components.
    """

    def __init__(self) -> None:
        """
        Initialize the container with empty path strings.
        """
        self._fullchain: str =""
        self._rootca: str = ""
        self._private_key: str = ""

    @property
    def fullchain(self) -> str:
        """
        Access the full path to the certificate chain **(rw)**.

        :param value: The file path to the certificate chain.
        :returns: The string path of the fullchain file.
        """
        return self._fullchain

    @fullchain.setter
    def fullchain(self, value: str):
        """
        Access the full path to the certificate chain **(rw)**.

        :param value: The file path to the certificate chain.
        :returns: The string path of the fullchain file.
        """
        self._fullchain = value

    @property
    def rootca(self) ->str:
        """
        Access the full path to the root certificate authority **(rw)**.

        :param value: The file path to the root CA.
        :returns: The string path of the root CA file.
        """
        return self._rootca

    @rootca.setter
    def rootca(self, value: str) -> None:
        """
        Access the full path to the root certificate authority **(rw)**.

        :param value: The file path to the root CA.
        :returns: The string path of the root CA file.
        """
        self._rootca = value

    @property
    def private_key(self) -> str:
        """
        Access the full path to the private key **(rw)**.

        :param value: The file path to the private key.
        :returns: The string path of the private key file.
        """
        return self._private_key

    @private_key.setter
    def private_key(self, value: str) -> None:
        """
        Access the full path to the private key **(rw)**.

        :param value: The file path to the private key.
        :returns: The string path of the private key file.
        """
        self._private_key = value

    def __setitem__(self, key:str,value:str) -> None:
        """
        Set a path for a specific component using a key.

        :param key: The name of the component.
        :param value: The path string to be assigned.
        """
        return setattr(self, f"_{key}", value)

    def __contains__(self, item:str) -> bool:
        """
        Check if a component name exists in the container slots.

        :param item: The name of the component to check.
        :returns: True if the component is defined in slots, False otherwise.
        """
        return f"_{item}" in self.__slots__


class RemoteContent(RemoteKeys):
    """
    Class to store the actual cryptographic content of remote components.
    """

    def __init__(self) -> None:
        """
        Initialize the container with empty cryptographic objects.
        """
        self._fullchain:list[Certificate]=[]
        self._rootca:Certificate|None = None
        self._private_key:RSAPrivateKey|None = None

    @property
    def fullchain(self) -> list[Certificate]:
        """
        Access the list of certificates in the chain **(rw)**.

        :param value: The list of certificates to be stored in the chain.
        :returns: The current list of certificates.
        """
        return self._fullchain

    @fullchain.setter
    def fullchain(self, value:list[Certificate]) -> None:
        """
        Access the list of certificates in the chain **(rw)**.

        :param value: The list of certificates to be stored in the chain.
        :returns: The current list of certificates.
        """
        self._fullchain= value

    @property
    def rootca(self) -> Certificate|None:
        """
        Access the root certificate authority object **(rw)**.

        :param value: The certificate object to be set as root CA.
        :returns: The root CA certificate or None if not set.
        """
        return self._rootca

    @rootca.setter
    def rootca(self, value: Certificate) -> None:
        """
        Access the root certificate authority object **(rw)**.

        :param value: The certificate object to be set as root CA.
        :returns: The root CA certificate or None if not set.
        """
        self._rootca = value

    @property
    def private_key(self) -> RSAPrivateKey | None:
        """
        Access the RSA private key object **(rw)**.

        :param value: The RSA private key object to be stored.
        :returns: The private key or None if not set.
        """
        return self._private_key

    @private_key.setter
    def private_key(self, value: RSAPrivateKey) -> None:
        """
        Access the RSA private key object **(rw)**.

        :param value: The RSA private key object to be stored.
        :returns: The private key or None if not set.
        """
        self._private_key = value

    @property
    def fullchainPEM(self) -> bytes:
        """
        Access the certificate chain in PEM format **(ro)**.

        :returns: The validated and formatted PEM bytes of the chain.
        """
        fullchain = [c.public_bytes(Encoding.PEM) for c in self._fullchain if c]
        return validate_and_format_chain(*fullchain)

    @property
    def fullchainDER(self) -> bytes:
        """
        Access the certificate chain in DER format **(ro)**.

        :returns: The concatenated DER bytes of the chain.
        """
        fullchain = [c.public_bytes(Encoding.DER) for c in self._fullchain if c]
        return b"".join(fullchain)

    @property
    def rootcaPEM(self) -> bytes | None:
        """
        Access the root CA in PEM format **(ro)**.

        :returns: The PEM bytes of the root CA or None.
        """
        return self._rootca.public_bytes(Encoding.PEM) if self._rootca is not None else None

    @property
    def rootcaDER(self) -> bytes | None:
        """
        Access the root CA in DER format **(ro)**.

        :returns: The DER bytes of the root CA or None.
        """
        return self._rootca.public_bytes(Encoding.DER) if self._rootca is not None else None

    @property
    def private_keyPEM(self) -> bytes | None:
        """
        Access the private key in PEM format **(ro)**.

        :returns: The unencrypted PKCS8 PEM bytes of the private key.
        """
        return self._private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption(),  # Oder BestAlgorithm(password)
        ) if self._private_key is not None else None

    @property
    def private_keyDER(self) -> bytes | None:
        """
        Access the private key in DER format **(ro)**.

        :returns: The unencrypted PKCS8 DER bytes of the private key.
        """
        return (
            self._private_key.private_bytes(
                encoding=Encoding.DER,
                format=PrivateFormat.PKCS8,
                encryption_algorithm=NoEncryption(),  # Oder BestAlgorithm(password)
            )
            if self._private_key is not None
            else None
        )


    def getPEM(self, key:str)->bytes:
        """
        Retrieve the PEM-encoded bytes for a specific component.

        :param key: The name of the component (e.g., 'private_key').
        :returns: The PEM bytes of the requested component.
        """
        return getattr(self, f"{key}PEM")

    def getDER(self, key: str) -> bytes:
        """
        Retrieve the DER-encoded bytes for a specific component.

        :param key: The name of the component (e.g., 'rootca').
        :returns: The DER bytes of the requested component.
        """
        return getattr(self, f"{key}DER")


class PKIRemoteContainer:
    """
    Main container for managing remote PKI data and file system attributes.
    """
    __slots__ = ["_encoding", "_usr", "_grp", "_file_path", "_content"]
    _dirmap = {"private_key": ".key", "fullchain": ".chain", "rootca": ".crt"}

    def __init__(self, encoding:Literal['PEM', 'DER']="PEM") -> None:
        """
        Initialize the container with specific encoding and empty components.

        :param encoding: The format used for cryptographic data (PEM or DER).
        """

        self._encoding:str = encoding
        self._usr:str = ""
        self._grp:str = ""
        self._file_path:RemotePathes = RemotePathes()
        self._content: RemoteContent = RemoteContent()

    @property
    def fullchain(self) -> list[Certificate]:
        """
        Access the certificate chain list **(rw)**.

        :param value: A list of certificate objects for the chain.
        :returns: The current list of certificates.
        """
        return self._content.fullchain

    
    @fullchain.setter
    def fullchain(self, value:list[Certificate]) -> None:
        """
        Access the certificate chain list **(rw)**.

        :param value: A list of certificate objects for the chain.
        :returns: The current list of certificates.
        """
        self._content.fullchain = value
        

    @property
    def private_key(self) -> RSAPrivateKey | None:
        """
        Access the RSA private key object **(rw)**.

        :param value: The private key object to be stored.
        :returns: The RSA private key or None if not set.
        """
        return self._content.private_key
    
    @private_key.setter
    def private_key(self, value:RSAPrivateKey) -> None:
        """
        Access the RSA private key object **(rw)**.

        :param value: The private key object to be stored.
        :returns: The RSA private key or None if not set.
        """
        self._content.private_key = value


    @property
    def caroot_cert(self)->Certificate|None:
        """
        Access the root CA certificate **(rw)**.

        :param value: The certificate object for the root CA.
        :returns: The root CA certificate or None.
        """
        return self._content.rootca

    @caroot_cert.setter
    def caroot_cert(self, value:Certificate) -> None:
        """
        Access the root CA certificate **(rw)**.

        :param value: The certificate object for the root CA.
        :returns: The root CA certificate or None.
        """
        self._content.rootca = value


    def load_pathes(self, content:bytes) -> None:
        """
        Load remote path configurations from TOML-formatted bytes.

        :param content: The binary content of the TOML configuration file.
        """
        ctx = tomllib.load(BytesIO(content))
        remote = ctx.get("remote", {})
        self._usr = remote.get('web_usr',"")
        self._grp = remote.get("web_grp", "")
        pathes:dict[str,str]= remote.get("path",{})
        names: dict[str, str] = remote.get("name", {})
        for k, v in pathes.items():
             name = names.get(k, "")
             name = name if name else f"{k}{self._dirmap[k]}"
             self._file_path[k] = "/".join([v, name])

    def save(self, filename:str|Path) -> None:
        """
        Save the cryptographic components into a ZIP archive.

        :param filename: The target path or name of the ZIP file.
        :raises PKIMissingExportPathError: If a required export path is missing.
        """
        zip_buffer = BytesIO()
        existing_dirs = set()
        with ZipFile(zip_buffer, mode="w", compression=ZIP_DEFLATED) as zf:
            for key in self._file_path.keys():
                file_path:str = self._file_path[key]
                if not file_path:
                    raise PKIMissingExportPathError(f"At least path for {key} is empty.")
                file_path_parent:str = file_path.rsplit("/", 1)[0]
                file_path = f"{file_path}.{self._encoding.lower()}"
                if file_path_parent not in existing_dirs:
                    zf.mkdir(file_path_parent)
                    existing_dirs.add(file_path_parent)
                content:bytes = (
                    self._content.getPEM(key)
                    if self._encoding == "PEM"
                    else self._content.getDER(key)
                )
                zf.writestr(file_path, content)
        target_path = Path(filename).with_suffix(".zip")
        target_path.write_bytes(zip_buffer.getvalue())



if __name__ == "__main__": # pragma: no cover
    from doctest import FAIL_FAST, testfile
    
    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    passed_files = 0
    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_files = [
        "get_started_container.rst",
    ]
    for file in test_files:
        test_file = testfiles_dir / file
        if test_file.exists():
            print(f"--- Running Doctest for {test_file.name} ---")
            doctestresult = testfile(
                str(test_file),
                module_relative=False,
                verbose=be_verbose,
                optionflags=option_flags,
            )
            test_failed += doctestresult.failed
            test_sum += doctestresult.attempted
            if doctestresult.failed > 0 and option_flags & FAIL_FAST:
                print(f"Doctest result for {test_file.name}: {doctestresult}")
                print(f"\nKeep going! You already passed {passed_files} files "
                  f"with {test_sum} tests before this hit.")                
                break  # Stop on first failure if FAIL_FAST is set
            passed_files += 1
        else:
            print(f"⚠️ Warning: Test file {test_file.name} not found.")
    if test_failed == 0:
        print(f"\nDocTests passed without errors, {test_sum} tests.")
    else:
        if not option_flags & FAIL_FAST:
            print(f"\nDocTests failed: {test_failed} tests out of {test_sum}.")
