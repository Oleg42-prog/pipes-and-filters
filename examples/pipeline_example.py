from pipes_and_filters import Pipeline
from pipes_and_filters import Pipe

# Caesar cipher

text = 'Hello'
key = 5

encrypt_pipeline = Pipeline(
    source=text,
    pipe=Pipe(
        ord,
        lambda x: x + key,
        chr
    )
)

encrypted_text = ''.join(encrypt_pipeline())

decrypt_pipeline = Pipeline(
    source=encrypted_text,
    pipe=Pipe(
        ord,
        lambda x: x - key,
        chr
    )
)

decrypted_text = ''.join(decrypt_pipeline())


print('Original text:', text)
print('Encrypted text:', encrypted_text)
print('Decrypted text:', decrypted_text)
