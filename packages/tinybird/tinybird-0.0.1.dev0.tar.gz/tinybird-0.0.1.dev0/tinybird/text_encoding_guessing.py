from typing import Tuple

import chardet
from chardet.charsetgroupprober import CharSetGroupProber
from chardet.universaldetector import UniversalDetector

"""
Chardet sometimes fails to detect UTF-8 and may return ISO-8859-1 in some cases.

Related issues:
https://github.com/chardet/chardet/issues/138
https://github.com/chardet/chardet/issues/134

Looks like one of the solutions is on the go: https://github.com/chardet/chardet/pull/153, but for now we may
need to do some changes, as the one suggested in https://github.com/chardet/chardet/pull/153#issuecomment-394145028.
This isn't a definitive fix, so we must follow this ticket and update the library with the fix.
"""
chardet.utf8prober.UTF8Prober.ONE_CHAR_PROB = 0.26  # type: ignore


def detect_all(block: bytes):
    """
    detect all possible encodings given a byte array
    """
    detector = UniversalDetector()
    detector.feed(block)
    detector.close()
    probs = []
    for group_prober in detector._charset_probers:  # type: ignore
        if not group_prober:
            continue
        if isinstance(group_prober, CharSetGroupProber):
            for prober in group_prober.probers:
                probs.append(
                    {
                        "encoding": prober.charset_name,
                        "confidence": prober.get_confidence(),
                        "language": prober.language,
                    }
                )
        else:
            probs.append(
                {
                    "encoding": group_prober.charset_name,
                    "confidence": group_prober.get_confidence(),
                    "language": group_prober.language,
                }
            )
    return probs


def decode_with_guess_brute_force(block: bytes):
    for x in sorted(detect_all(block), key=lambda x: x["confidence"]):
        try:
            data = block.decode(x["encoding"])
            return data, x["encoding"]
        except UnicodeDecodeError:
            pass
        except LookupError:
            # unknown encoding
            pass
    raise UnicodeDecodeError("tried every possible charset and failed")  # type: ignore


def try_decode_block(block: bytes, encoding: str):
    """
    try using specified encoding, if that fails try to guess other encodings and test them
    """
    try:
        return block.decode(encoding)
    except UnicodeDecodeError:
        for x in sorted(detect_all(block), key=lambda x: x["confidence"]):
            try:
                return block.decode(x["encoding"])
            except UnicodeDecodeError:
                pass
        raise UnicodeDecodeError("tried every possible charset and failed")  # type: ignore


def decode_with_guess(csv_extract: bytes, ignore_last_incomplete_char: bool = True) -> Tuple[str, str]:
    """
    >>> decode_with_guess(b'abc')
    ('abc', 'utf-8')
    >>> decode_with_guess(b'.. .. ..')[1]
    'utf-8'
    >>> decode_with_guess('© Foto'.encode("utf8"))[1]
    'utf-8'
    >>> decode_with_guess('© Foto ©'.encode("utf8"))[1]
    'utf-8'
    >>> decode_with_guess('date,status,version,json,"{""searchTerm"":""jersey-basico-manga-abullonada"",""article"":{""code"":""502626433-444"",""brand"":""pull-and-bear"",""store"":""pull-and-bear"",""name"":""Jersey básico manga abullonada"",""photo"":""https://static.pullandbear.net/2/photos/2021/V/0/1/p/9553/304/444/9553304444_2_1_2.jpg?t=1610473025354"",""price"":19.99,""link"":""https://www.pullandbear.com/es/es/woman-c1030204572p502626433.html?cS=444"",""hash"":""pull-and-bear__502626433-444""}}'.encode("utf8"))[1]
    'utf-8'
    >>> decode_with_guess('Text in 8859-1 @téxt téstïng'.encode("ISO-8859-1"))[1]
    'ISO-8859-1'
    >>> decode_with_guess('Text in utf-8 @téxt téstïng'.encode("utf-8"))[1]
    'utf-8'
    >>> decode_with_guess("I'm: bored 😑 ".encode("utf-8"))[1]
    'utf-8'
    >>> decode_with_guess(b'a'*10000 + b'\\xd9')[1]
    'utf-8'
    >>> decode_with_guess(b'a'*9999 + b'\\xf0\\x92')[1]
    'utf-8'
    """
    try:
        data = csv_extract.decode("utf-8")
        return data, "utf-8"
    except UnicodeDecodeError as error:
        # csv_extract may have cut the last character
        # utf-8 has a max character size of 4 bytes
        # therefore, if last 3 bytes cannot be decoded, that
        # may be due to the cut
        if ignore_last_incomplete_char and error.start >= (len(csv_extract) - 3):
            return csv_extract[: error.start].decode("utf-8"), "utf-8"

    try:
        encoding = chardet.detect(csv_extract)["encoding"]
        if encoding:
            data = csv_extract.decode(encoding)
            return data, encoding
    except UnicodeDecodeError:
        pass

    return decode_with_guess_brute_force(csv_extract)
