import pytest
from unittest.mock import patch
import os
from eth_account import Account
from footium_api.key_signer import KeySigner

@pytest.fixture
def generated_account():
    # Generate a new Ethereum account
    account = Account.create()
    return {
        "address": account.address.lower(),
        "private_key": account.key.hex()
    }

@pytest.fixture
def key_signer(generated_account):
    with patch.dict(os.environ, {f"_{generated_account['address']}": generated_account['private_key']}):
        return KeySigner(generated_account['address'])

def test_initialization_success(generated_account):
    eth_address = generated_account['address']
    private_key = generated_account['private_key']
    with patch.dict(os.environ, {f"_{eth_address}": private_key}):
        signer = KeySigner(eth_address)
        assert signer.eth_address == eth_address
        assert signer.private_key_hex == private_key

def test_initialization_failure(generated_account):
    eth_address = generated_account['address']
    with patch.dict(os.environ, {f"_{eth_address}": ""}):
        with pytest.raises(RuntimeError, match=f"Private key for {eth_address} is not set."):
            KeySigner(eth_address)

def test_sign_message(key_signer):
    message = "Hello, Ethereum!"
    signature = key_signer.sign_message(message)
    assert signature.startswith("0x")

def test_validate_signed_message(key_signer):
    message = "Hello, Ethereum!"
    signature = key_signer.sign_message(message)
    is_valid = key_signer.validate_signed_message(signature, message)
    assert is_valid

def test_validate_invalid_signature(key_signer):
    message = "Hello, Ethereum!"
    invalid_signature = "0x" + "0" * 130  # an obviously invalid signature
    is_valid = key_signer.validate_signed_message(invalid_signature, message)
    assert not is_valid

def test_get_eth_address(key_signer, generated_account):
    assert key_signer.get_eth_address() == generated_account['address']
