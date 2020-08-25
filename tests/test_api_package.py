"""
    test_api_package
    ~~~~~~~~~~~~~~~~

    Tests for the :pkg:`~ulid.api` package interface.
"""
import datetime
import time
import uuid

import pytest

from ulid import base32, consts, ulid
from ulid.api import default, monotonic
from ulid.api.api import ALL

BYTES_SIZE_EXC_REGEX = r'Expects bytes to be 128 bits'
INT_SIZE_EXC_REGEX = r'Expects integer to be 128 bits'
INT_NEGATIVE_EXC_REGEX = r'Expects positive integer'
STR_SIZE_EXC_REGEX = r'Expects 26 characters'
UNSUPPORTED_TIMESTAMP_TYPE_EXC_REGEX = (r'Expected datetime, int, float, str, memoryview, Timestamp'
                                        r', ULID, bytes, or bytearray')
TIMESTAMP_SIZE_EXC_REGEX = r'Expects timestamp to be 48 bits'
UNSUPPORTED_RANDOMNESS_TYPE_EXC_REGEX = r'Expected int, float, str, memoryview, Randomness, ULID, bytes, or bytearray'
RANDOMNESS_SIZE_EXC_REGEX = r'Expects randomness to be 80 bits'

PARSE_STR_LEN_EXC_REGEX = r'^Cannot create ULID from string of length '
PARSE_UNSUPPORTED_TYPE_REGEX = r'^Cannot create ULID from type'


@pytest.fixture(scope='module', params=[
    default,
    monotonic
])
def api(request):
    """
    Fixture that yields a :class:`~ulid.api.api.Api` instance.
    """
    return request.param


@pytest.fixture(scope='module', params=[
    list,
    dict,
    set,
    tuple,
    type(None)
])
def unsupported_type(request):
    """
    Fixture that yields types that a cannot be converted to a timestamp/randomness.
    """
    return request.param


@pytest.fixture(scope='module', params=[bytes, bytearray, memoryview])
def buffer_type(request):
    """
    Fixture that yields types that support the buffer protocol.
    """
    return request.param


def test_package_has_dunder_all(api):
    """
    Assert that :pkg:`~ulid.api` exposes the :attr:`~ulid.api.__all__` attribute as a list.
    """
    assert hasattr(api, '__all__')
    assert isinstance(api.__all__, list)


def test_package_exposes_expected_interface(api):
    """
    Assert that :attr:`~ulid.providers.__all__` exposes expected interface.
    """
    assert api.__all__ == ALL


def test_min_timestamp_uses_expected_value(api):
    """
    Assert that :func:`~ulid.api.MIN_TIMESTAMP` uses expected byte value.
    """
    value = api.MIN_TIMESTAMP
    assert value == consts.MIN_TIMESTAMP


def test_max_timestamp_uses_expected_value(api):
    """
    Assert that :func:`~ulid.api.MAX_RANDOMNESS` uses expected byte value.
    """
    value = api.MAX_TIMESTAMP
    assert value == consts.MAX_TIMESTAMP


def test_min_randomness_uses_expected_value(api):
    """
    Assert that :func:`~ulid.api.MIN_RANDOMNESS` uses expected byte value.
    """
    value = api.MIN_RANDOMNESS
    assert value == consts.MIN_RANDOMNESS


def test_max_randomness_uses_expected_value(api):
    """
    Assert that :func:`~ulid.api.MAX_RANDOMNESS` uses expected byte value.
    """
    value = api.MAX_RANDOMNESS
    assert value == consts.MAX_RANDOMNESS


def test_min_ulid_uses_expected_value(api):
    """
    Assert that :func:`~ulid.api.MIN_ULID` uses expected byte value.
    """
    value = api.MIN_ULID
    assert value == consts.MIN_ULID


def test_max_ulid_uses_expected_value(api):
    """
    Assert that :func:`~ulid.api.MAX_ULID` uses expected byte value.
    """
    value = api.MAX_ULID
    assert value == consts.MAX_ULID


def test_new_returns_ulid_instance(api):
    """
    Assert that :func:`~ulid.api.new` returns a new :class:`~ulid.ulid.ULID` instance.
    """
    assert isinstance(api.new(), ulid.ULID)


def test_parse_returns_given_ulid_instance(api):
    """
    Assert that :func:`~ulid.api.parse` returns the given :class:`~ulid.ulid.ULID` instance
    when given one.
    """
    value = api.new()
    instance = api.parse(value)
    assert isinstance(instance, ulid.ULID)
    assert instance == value


def test_parse_returns_ulid_instance_from_uuid(api):
    """
    Assert that :func:`~ulid.api.parse` returns a new :class:`~ulid.ulid.ULID` instance
    from the given :class:`~uuid.UUID`.
    """
    value = uuid.uuid4()
    instance = api.parse(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == value.bytes


def test_parse_returns_ulid_instance_from_uuid_str(api):
    """
    Assert that :func:`~ulid.api.parse` returns a new :class:`~ulid.ulid.ULID` instance
    from the given :class:`~uuid.UUID` instance in its string format.
    """
    value = uuid.uuid4()
    instance = api.parse(str(value))
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == value.bytes


def test_parse_returns_ulid_instance_from_uuid_hex_str(api):
    """
    Assert that :func:`~ulid.api.parse` returns a new :class:`~ulid.ulid.ULID` instance
    from the given :class:`~uuid.UUID` instance in its hex string format.
    """
    value = uuid.uuid4()
    instance = api.parse(value.hex)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == value.bytes


def test_parse_returns_ulid_instance_from_ulid_str(api, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.parse` returns a new :class:`~ulid.ulid.ULID` instance
    from the given :class:`~str` instance that represents a fill ULID.
    """
    value = base32.encode(valid_bytes_128)
    instance = api.parse(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == valid_bytes_128


def test_parse_returns_ulid_instance_from_randomness_str(api, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.parse` returns a new :class:`~ulid.ulid.ULID` instance
    from the given :class:`~str` instance that represents randomness data.
    """
    value = base32.encode_randomness(valid_bytes_80)
    instance = api.parse(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().str == value


def test_parse_returns_ulid_instance_from_timestamp_str(api, valid_bytes_48):
    """
    Assert that :func:`~ulid.api.parse` returns a new :class:`~ulid.ulid.ULID` instance
    from the given :class:`~str` instance that represents timestamp data.
    """
    value = base32.encode_timestamp(valid_bytes_48)
    instance = api.parse(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp().str == value


def test_parse_error_on_invalid_length_str(api, invalid_str_10_16_26_32_36):
    """
    Assert that :func:`~ulid.api.parse` returns a new :class:`~ulid.ulid.ULID` instance
    from the given :class:`~str` instance that represents timestamp data.
    """
    with pytest.raises(ValueError) as ex:
        api.parse(invalid_str_10_16_26_32_36)
    assert ex.match(PARSE_STR_LEN_EXC_REGEX)


def test_parse_returns_ulid_instance_from_int(api, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.parse` returns a new :class:`~ulid.ulid.ULID` instance
    from a valid ULID stored as an int.
    """
    value = int.from_bytes(valid_bytes_128, byteorder='big')
    instance = api.parse(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == valid_bytes_128


def test_parse_raises_when_int_greater_than_128_bits(api, invalid_bytes_128_overflow):
    """
    Assert that :func:`~ulid.api.parse` raises a :class:`~ValueError` when given int
    cannot be stored in 128 bits.
    """
    value = int.from_bytes(invalid_bytes_128_overflow, byteorder='big')
    with pytest.raises(ValueError) as ex:
        api.parse(value)
    assert ex.match(INT_SIZE_EXC_REGEX)


def test_parse_raises_when_int_negative(api):
    """
    Assert that :func:`~ulid.api.parse` raises a :class:`~ValueError` when given
    a negative int number.
    """
    with pytest.raises(ValueError) as ex:
        api.parse(-1)
    assert ex.match(INT_NEGATIVE_EXC_REGEX)


def test_parse_returns_ulid_instance_from_float(api, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.parse` returns a new :class:`~ulid.ulid.ULID` instance
    from a valid ULID stored as a float.
    """
    value = float(int.from_bytes(valid_bytes_128, byteorder='big'))
    instance = api.parse(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.int == int(value)


def test_parse_raises_when_float_greater_than_128_bits(api, invalid_bytes_128_overflow):
    """
    Assert that :func:`~ulid.api.parse` raises a :class:`~ValueError` when given float
    cannot be stored in 128 bits.
    """
    value = float(int.from_bytes(invalid_bytes_128_overflow, byteorder='big'))
    with pytest.raises(ValueError) as ex:
        api.parse(value)
    assert ex.match(INT_SIZE_EXC_REGEX)


def test_parse_raises_when_float_negative(api):
    """
    Assert that :func:`~ulid.api.parse` raises a :class:`~ValueError` when given
    a negative float number.
    """
    with pytest.raises(ValueError) as ex:
        api.parse(float(-1))
    assert ex.match(INT_NEGATIVE_EXC_REGEX)


def test_parse_returns_ulid_instance_from_buffer_type(api, buffer_type, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.parse` returns a new :class:`~ulid.ulid.ULID` instance
    from a valid set of 128 bytes representing by the given buffer type.
    """
    value = buffer_type(valid_bytes_128)
    instance = api.parse(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == valid_bytes_128


def test_parse_raises_when_buffer_type_not_128_bits(api, buffer_type, invalid_bytes_128):
    """
    Assert that :func:`~ulid.api.parse` raises a :class:`~ValueError` when given bytes
    that is not 128 bit in length.
    """
    value = buffer_type(invalid_bytes_128)
    with pytest.raises(ValueError) as ex:
        api.parse(value)
    assert ex.match(BYTES_SIZE_EXC_REGEX)


def test_parse_raises_when_given_unsupported_type(api, unsupported_type):
    """
    Assert that :func:`~ulid.api.parse` raises a :class:`~ValueError` when a value
    of an unsupported type.
    """
    with pytest.raises(ValueError) as ex:
        api.parse(unsupported_type)
    assert ex.match(PARSE_UNSUPPORTED_TYPE_REGEX)


def test_create_timestamp_datetime_returns_ulid_instance(api, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given Unix time from epoch in seconds as an :class:`~datetime.datetime`.
    """
    value = datetime.datetime.now()
    instance = api.create(value, valid_bytes_80)
    assert isinstance(instance, ulid.ULID)
    assert int(instance.timestamp().timestamp) == int(value.timestamp())


def test_create_timestamp_int_returns_ulid_instance(api, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given Unix time from epoch in seconds as an :class:`~int`.
    """
    value = int(time.time())
    instance = api.create(value, valid_bytes_80)
    assert isinstance(instance, ulid.ULID)
    assert int(instance.timestamp().timestamp) == value


def test_create_timestamp_float_returns_ulid_instance(api, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given Unix time from epoch in seconds as a :class:`~float`.
    """
    value = float(time.time())
    instance = api.create(value, valid_bytes_80)
    assert isinstance(instance, ulid.ULID)
    assert int(instance.timestamp().timestamp) == int(value)


def test_create_timestamp_str_returns_ulid_instance(api, valid_bytes_48, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as a :class:`~str`.
    """
    value = base32.encode_timestamp(valid_bytes_48)
    instance = api.create(value, valid_bytes_80)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp().str == value


def test_create_timestamp_bytes_returns_ulid_instance(api, buffer_type, valid_bytes_48, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as an object that supports the buffer protocol.
    """
    value = buffer_type(valid_bytes_48)
    instance = api.create(value, valid_bytes_80)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp().bytes == value


def test_create_timestamp_timestamp_returns_ulid_instance(api, valid_bytes_48, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as a :class:`~ulid.ulid.Timestamp`.
    """
    value = ulid.Timestamp(valid_bytes_48)
    instance = api.create(value, valid_bytes_80)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp() == value


def test_create_timestamp_ulid_returns_ulid_instance(api, valid_bytes_128, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as a :class:`~ulid.ulid.ULID`.
    """
    value = ulid.ULID(valid_bytes_128)
    instance = api.create(value, valid_bytes_80)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp() == value.timestamp()


def test_create_raises_when_given_unsupported_timestamp_type(api, unsupported_type, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` raises a :class:`~ValueError` when timestamp value
    of an unsupported type.
    """
    with pytest.raises(ValueError) as ex:
        api.create(unsupported_type, valid_bytes_80)
    assert ex.match(UNSUPPORTED_TIMESTAMP_TYPE_EXC_REGEX)


def test_create_randomness_int_returns_ulid_instance(api, valid_bytes_48, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an :class:`~int`.
    """
    value = int.from_bytes(valid_bytes_80, byteorder='big')
    instance = api.create(valid_bytes_48, value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().int == value


def test_create_randomness_float_returns_ulid_instance(api, valid_bytes_48, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an :class:`~float`.
    """
    value = float(int.from_bytes(valid_bytes_80, byteorder='big'))
    instance = api.create(valid_bytes_48, value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().int == int(value)


def test_create_randomness_str_returns_ulid_instance(api, valid_bytes_48, valid_bytes_80):

    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an :class:`~str`.
    """
    value = base32.encode_randomness(valid_bytes_80)
    instance = api.create(valid_bytes_48, value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().str == value


def test_create_randomness_bytes_returns_ulid_instance(api, buffer_type, valid_bytes_48, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an object that supports the buffer protocol.
    """
    value = buffer_type(valid_bytes_80)
    instance = api.create(valid_bytes_48, value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().bytes == value


def test_create_randomness_randomness_returns_ulid_instance(api, valid_bytes_48, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as a :class:`~ulid.ulid.Randomness`.
    """
    value = ulid.Randomness(valid_bytes_80)
    instance = api.create(valid_bytes_48, value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness() == value


def test_create_randomness_ulid_returns_ulid_instance(api, valid_bytes_48, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.create` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as a :class:`~ulid.ulid.ULID`.
    """
    value = ulid.ULID(valid_bytes_128)
    instance = api.create(valid_bytes_48, value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness() == value.randomness()


def test_create_raises_when_given_unsupported_randomness_type(api, unsupported_type, valid_bytes_48):
    """
    Assert that :func:`~ulid.api.create` raises a :class:`~ValueError` when randomness value
    of an unsupported type.
    """
    with pytest.raises(ValueError) as ex:
        api.create(valid_bytes_48, unsupported_type)
    assert ex.match(UNSUPPORTED_RANDOMNESS_TYPE_EXC_REGEX)


def test_from_bytes_returns_ulid_instance(api, buffer_type, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_bytes` returns a new :class:`~ulid.ulid.ULID` instance
    from the given bytes.
    """
    value = buffer_type(valid_bytes_128)
    instance = api.from_bytes(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == valid_bytes_128


def test_from_bytes_raises_when_not_128_bits(api, buffer_type, invalid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_bytes` raises a :class:`~ValueError` when given bytes
    that is not 128 bit in length.
    """
    value = buffer_type(invalid_bytes_128)
    with pytest.raises(ValueError) as ex:
        api.from_bytes(value)
    assert ex.match(BYTES_SIZE_EXC_REGEX)


def test_from_int_returns_ulid_instance(api, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_int` returns a new :class:`~ulid.ulid.ULID` instance
    from the given bytes.
    """
    value = int.from_bytes(valid_bytes_128, byteorder='big')
    instance = api.from_int(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == valid_bytes_128


def test_from_int_raises_when_greater_than_128_bits(api, invalid_bytes_128_overflow):
    """
    Assert that :func:`~ulid.api.from_int` raises a :class:`~ValueError` when given int
    cannot be stored in 128 bits.
    """
    value = int.from_bytes(invalid_bytes_128_overflow, byteorder='big')
    with pytest.raises(ValueError) as ex:
        api.from_int(value)
    assert ex.match(INT_SIZE_EXC_REGEX)


def test_from_int_raises_when_negative_number(api):
    """
    Assert that :func:`~ulid.api.from_int` raises a :class:`~ValueError` when given
    a negative number.
    """
    with pytest.raises(ValueError) as ex:
        api.from_int(-1)
    assert ex.match(INT_NEGATIVE_EXC_REGEX)


def test_from_str_returns_ulid_instance(api, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_str` returns a new :class:`~ulid.ulid.ULID` instance
    from the given bytes.
    """
    value = base32.encode(valid_bytes_128)
    instance = api.from_str(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == valid_bytes_128


def test_from_str_raises_when_not_128_bits(api, valid_bytes_48):
    """
    Assert that :func:`~ulid.api.from_str` raises a :class:`~ValueError` when given bytes
    that is not 128 bit in length.
    """
    value = base32.encode(valid_bytes_48)
    with pytest.raises(ValueError) as ex:
        api.from_str(value)
    assert ex.match(STR_SIZE_EXC_REGEX)


def test_from_uuid_returns_ulid_instance(api):
    """
    Assert that :func:`~ulid.api.from_uuid` returns a new :class:`~ulid.ulid.ULID` instance
    from the underlying bytes of the UUID.
    """
    value = uuid.uuid4()
    instance = api.from_uuid(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.bytes == value.bytes


def test_from_timestamp_datetime_returns_ulid_instance(api):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given Unix time from epoch in seconds as an :class:`~datetime.datetime`.
    """
    value = datetime.datetime.now()
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert int(instance.timestamp().timestamp) == int(value.timestamp())


def test_from_timestamp_int_returns_ulid_instance(api):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given Unix time from epoch in seconds as an :class:`~int`.
    """
    value = int(time.time())
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert int(instance.timestamp().timestamp) == value


def test_from_timestamp_float_returns_ulid_instance(api):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given Unix time from epoch in seconds as a :class:`~float`.
    """
    value = float(time.time())
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert int(instance.timestamp().timestamp) == int(value)


def test_from_timestamp_str_returns_ulid_instance(api, valid_bytes_48):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as a :class:`~str`.
    """
    value = base32.encode_timestamp(valid_bytes_48)
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp().str == value


def test_from_timestamp_bytes_returns_ulid_instance(api, buffer_type, valid_bytes_48):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as an object that supports the buffer protocol.
    """
    value = buffer_type(valid_bytes_48)
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp().bytes == value


def test_from_timestamp_timestamp_returns_ulid_instance(api, valid_bytes_48):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as a :class:`~ulid.ulid.Timestamp`.
    """
    value = ulid.Timestamp(valid_bytes_48)
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp() == value


def test_from_timestamp_ulid_returns_ulid_instance(api, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_timestamp` returns a new :class:`~ulid.ulid.ULID` instance
    from the given timestamp as a :class:`~ulid.ulid.ULID`.
    """
    value = ulid.ULID(valid_bytes_128)
    instance = api.from_timestamp(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.timestamp() == value.timestamp()


def test_from_timestamp_with_unsupported_type_raises(api, unsupported_type):
    """
    Assert that :func:`~ulid.api.from_timestamp` raises a :class:`~ValueError` when given
    a type it cannot compute a timestamp value from.
    """
    with pytest.raises(ValueError) as ex:
        api.from_timestamp(unsupported_type())
    assert ex.match(UNSUPPORTED_TIMESTAMP_TYPE_EXC_REGEX)


def test_from_timestamp_with_incorrect_size_bytes_raises(api, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_timestamp` raises a :class:`~ValueError` when given
    a type that cannot be represented as exactly 48 bits.
    """
    with pytest.raises(ValueError) as ex:
        api.from_timestamp(valid_bytes_128)
    assert ex.match(TIMESTAMP_SIZE_EXC_REGEX)


def test_from_randomness_int_returns_ulid_instance(api, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an :class:`~int`.
    """
    value = int.from_bytes(valid_bytes_80, byteorder='big')
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().int == value


def test_from_randomness_float_returns_ulid_instance(api, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an :class:`~float`.
    """
    value = float(int.from_bytes(valid_bytes_80, byteorder='big'))
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().int == int(value)


def test_from_randomness_str_returns_ulid_instance(api, valid_bytes_80):

    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an :class:`~str`.
    """
    value = base32.encode_randomness(valid_bytes_80)
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().str == value


def test_from_randomness_bytes_returns_ulid_instance(api, buffer_type, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as an object that supports the buffer protocol.
    """
    value = buffer_type(valid_bytes_80)
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness().bytes == value


def test_from_randomness_randomness_returns_ulid_instance(api, valid_bytes_80):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as a :class:`~ulid.ulid.Randomness`.
    """
    value = ulid.Randomness(valid_bytes_80)
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness() == value


def test_from_randomness_ulid_returns_ulid_instance(api, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_randomness` returns a new :class:`~ulid.ulid.ULID` instance
    from the given random values as a :class:`~ulid.ulid.ULID`.
    """
    value = ulid.ULID(valid_bytes_128)
    instance = api.from_randomness(value)
    assert isinstance(instance, ulid.ULID)
    assert instance.randomness() == value.randomness()


def test_from_randomness_with_unsupported_type_raises(api, unsupported_type):
    """
    Assert that :func:`~ulid.api.from_randomness` raises a :class:`~ValueError` when given
    a type it cannot compute a randomness value from.
    """
    with pytest.raises(ValueError) as ex:
        api.from_randomness(unsupported_type())
    assert ex.match(UNSUPPORTED_RANDOMNESS_TYPE_EXC_REGEX)


def test_from_randomness_with_incorrect_size_bytes_raises(api, valid_bytes_128):
    """
    Assert that :func:`~ulid.api.from_randomness` raises a :class:`~ValueError` when given
    a type that cannot be represented as exactly 80 bits.
    """
    with pytest.raises(ValueError) as ex:
        api.from_randomness(valid_bytes_128)
    assert ex.match(RANDOMNESS_SIZE_EXC_REGEX)
