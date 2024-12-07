Convenience hashing facilities.

*Latest release 20241207*:
BaseHashCode.hashclass: raise ValueError from unknown hash function name with greater detail on the underlying failure.

## <a name="BaseHashCode"></a>Class `BaseHashCode(builtins.bytes)`

Base class for hashcodes, subclassed by `SHA1`, `SHA256` et al.

You can obtain the class for a particular hasher by name, example:

    SHA256 = BaseHashCode.hashclass('sha256')

*`BaseHashCode.__str__(self)`*:
Return `f'{self.hashname}:{self.hex()}'`.

*`BaseHashCode.from_buffer(bfr: cs.buffer.CornuCopyBuffer)`*:
Compute hashcode from the contents of the `CornuCopyBuffer` `bfr`.

*`BaseHashCode.from_data(bs)`*:
Compute hashcode from the data `bs`.

*`BaseHashCode.from_fspath(fspath, **kw)`*:
Compute hashcode from the contents of the file `fspath`.

*`BaseHashCode.from_hashbytes(hashbytes)`*:
Factory function returning a `BaseHashCode` object from the hash bytes.

*`BaseHashCode.from_hashbytes_hex(hashhex: str)`*:
Factory function returning a `BaseHashCode` object
from the hash bytes hex text.

*`BaseHashCode.from_named_hashbytes_hex(hashname, hashhex)`*:
Factory function to return a `HashCode` object
from the hash type name and the hash bytes hex text.

*`BaseHashCode.from_prefixed_hashbytes_hex(hashtext: str)`*:
Factory function returning a `BaseHashCode` object
from the hash bytes hex text prefixed by the hashname.
This is the reverse of `__str__`.

*`BaseHashCode.get_hashfunc(hashname: str)`*:
Fetch the hash function implied by `hashname`.

*`BaseHashCode.hashclass(hashname: str, hashfunc=None, **kw)`*:
Return the class for the hash function named `hashname`.

Parameters:
* `hashname`: the name of the hash function
* `hashfunc`: optional hash function for the class

*`BaseHashCode.hashname`*:
The hash code type name, derived from the class name.

*`BaseHashCode.hex(self) -> str`*:
Return the hashcode bytes transcribes as a hexadecimal ASCII `str`.

*`BaseHashCode.promote(obj)`*:
Promote to a `BaseHashCode` instance.

## <a name="MD5"></a>Class `MD5(BaseHashCode)`

Hash class for the 'md5' algorithm.

*`MD5.hashfunc`*

## <a name="SHA1"></a>Class `SHA1(BaseHashCode)`

Hash class for the 'sha1' algorithm.

*`SHA1.hashfunc`*

## <a name="SHA224"></a>Class `SHA224(BaseHashCode)`

Hash class for the 'sha224' algorithm.

*`SHA224.hashfunc`*

## <a name="SHA256"></a>Class `SHA256(BaseHashCode)`

Hash class for the 'sha256' algorithm.

*`SHA256.hashfunc`*

## <a name="SHA384"></a>Class `SHA384(BaseHashCode)`

Hash class for the 'sha384' algorithm.

*`SHA384.hashfunc`*

## <a name="SHA512"></a>Class `SHA512(BaseHashCode)`

Hash class for the 'sha512' algorithm.

*`SHA512.hashfunc`*

# Release Log



*Release 20241207*:
BaseHashCode.hashclass: raise ValueError from unknown hash function name with greater detail on the underlying failure.

*Release 20240412*:
* BaseHashCode.hashclass(hashname): fall back to looking for blake3 from the blake3 module.
* BaseHashCode: new get_hashfunc(hashname) static method.

*Release 20240316*:
Fixed release upload artifacts.

*Release 20240211*:
Initial PyPI release: BaseHashCode(bytes) and subclasses for various hash algorithms.
