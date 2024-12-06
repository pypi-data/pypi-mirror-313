from .venumpy import small_glwe_bindings as _bindings

class Ciphertext:
    """
    Represents an encrypted ciphertext in the cryptographic scheme.

    This class allows for homomorphic operations (addition, subtraction, 
    multiplication) on ciphertexts and supports serialization to/from JSON format.

    Attributes
    ----------
    _raw_cipher : object
        The underlying raw ciphertext from the bindings.
    _context : object
        The context in which the ciphertext was created (either public or secret).
    """

    def __init__(self, raw_cipher, context):
        """
        Initializes a new ciphertext from a raw ciphertext and context.

        Parameters
        ----------
        raw_cipher : object
            The raw ciphertext object from the bindings.
        context : object
            The context associated with the ciphertext.
        """
        self._raw_cipher = raw_cipher
        self._context = context

    def decrypt(self):
        """
        Decrypts a ciphertext.

        Returns
        -------
        object
            The decrypted value.
        """
        return self._context.decrypt(self)

    def __add__(self, rhs):
        """
        Performs homomorphic addition between two ciphertexts.

        Parameters
        ----------
        rhs : Ciphertext
            The right-hand side Ciphertext to add.

        Returns
        -------
        Ciphertext
            A new Ciphertext representing the result of the addition.
        """
        raw_result = self._context._raw_ctx.add(self._raw_cipher, rhs._raw_cipher)
        return Ciphertext(raw_result, self._context)

    def __sub__(self, rhs):
        """
        Performs homomorphic subtraction between two ciphertexts.

        Parameters
        ----------
        rhs : Ciphertext
            The right-hand side Ciphertext to subtract.

        Returns
        -------
        Ciphertext
            A new Ciphertext representing the result of the subtraction.
        """
        raw_result = self._context._raw_ctx.sub(self._raw_cipher, rhs._raw_cipher)
        return Ciphertext(raw_result, self._context)

    def __mul__(self, rhs):
        """
        Performs homomorphic multiplication between two ciphertexts.

        Parameters
        ----------
        rhs : Ciphertext
            The right-hand side Ciphertext to multiply.

        Returns
        -------
        Ciphertext
            A new Ciphertext representing the result of the multiplication.
        """
        raw_result = self._context._raw_ctx.mul(self._raw_cipher, rhs._raw_cipher)
        return Ciphertext(raw_result, self._context)

    def __truediv__(self, rhs):
        """
        Performs homomorphic division of a ciphertext by a scalar.

        Parameters
        ----------
        rhs : int or float
            The scalar value to divide by.

        Returns
        -------
        Ciphertext
            A new Ciphertext representing the result of the division.
        """
        raw_result = self._context._raw_ctx.div_by_scalar(self._raw_cipher, rhs)
        return Ciphertext(raw_result, self._context)

    def __pow__(self, exponent):
        """
        Performs homomorphic exponentiation of a ciphertext with a given exponent.

        Parameters
        ----------
        exponent : int
            The exponent to raise the ciphertext to.

        Returns
        -------
        Ciphertext
            A new Ciphertext representing the result of the exponentiation.

        Raises
        ------
        TypeError
            If `exponent` is not an integer.
        ValueError
            If `exponent` is less than 1.
        """
        if not isinstance(exponent, int):
            raise TypeError("`exponent` must be an integer")
        if exponent < 1:
            raise ValueError("`exponent` must be strictly greater than 0")
        acc = self
        for _ in range(1, exponent):
            acc = acc * acc
        return acc

    def into_json(self):
        """
        Serializes the ciphertext into a JSON format.

        Returns
        -------
        str
            A JSON string representation of the ciphertext.
        """
        return self._raw_cipher.as_json()

    @staticmethod
    def from_json(context, cipher_json):
        """
        Deserializes a JSON representation of a ciphertext.

        Parameters
        ----------
        context : object
            The context to associate with the deserialized Ciphertext.
        cipher_json : str
            The JSON string representing the ciphertext.

        Returns
        -------
        Ciphertext
            A new Ciphertext object.
        """
        raw_cipher = _bindings.Ciphertext.from_json(cipher_json)
        return Ciphertext(raw_cipher, context)

    def into_bytes(self):
        """
        Serializes the ciphertext into bytes.

        Returns
        -------
        bytes
            A byte representation of the ciphertext.
        """
        return self._raw_cipher.as_bytes()

    @staticmethod
    def from_bytes(context, cipher_bytes):
        """
        Deserializes a byte representation of a ciphertext.

        Parameters
        ----------
        context : object
            The context to associate with the deserialized Ciphertext.
        cipher_bytes : bytes
            The bytes representing the ciphertext.

        Returns
        -------
        Ciphertext
            A new Ciphertext object.
        """
        raw_cipher = _bindings.Ciphertext.from_bytes(cipher_bytes)
        return Ciphertext(raw_cipher, context)


class Context:
    """
    Represents a general cryptographic context.

    Provides methods to serialize and manage the precision of computations.

    Attributes
    ----------
    _raw_ctx : object
        The raw context object from the bindings.
    """

    def __init__(self):
        pass

    @classmethod
    def _from_raw(cls, raw_ctx):
        """
        Reconstructs a context from a raw context.

        Parameters
        ----------
        raw_ctx : object
            The raw context.

        Returns
        -------
        Context
            A new context object.
        """
        ctx = cls(generate=False)
        ctx._raw_ctx = raw_ctx
        return ctx

    def into_json(self):
        """
        Serializes the context into a JSON format.

        Returns
        -------
        str
            A JSON string representation of the context.
        """
        return self._raw_ctx.as_json()

    def into_bytes(self):
        """
        Serializes the context into a byte format.

        Returns
        -------
        bytes
            A byte representation of the context.
        """
        return self._raw_ctx.as_bytes()

    def _set_precision(self, precision):
        """
        Sets the floating point precision of the context.

        Parameters
        ----------
        precision : int
            The desired precision.

        Returns
        -------
        None
        """
        self._raw_ctx.set_precision(precision)

    def _get_precision(self):
        """
        Gets the floating point precision of the context.

        Returns
        -------
        int
            The current precision.
        """
        return self._raw_ctx.get_precision()

    precision = property(
        fget=_get_precision,
        fset=_set_precision,
        doc="Floating point precision."
    )


class SecretContext(Context):
    """
    Represents a secret cryptographic context, used for key generation and decryption.

    Attributes
    ----------
    _raw_ctx : object
        The underlying raw secret context from the bindings.
    """

    def __init__(self, bits_of_security=128, generate=True):
        """
        Initializes a new secret context.

        Parameters
        ----------
        bits_of_security : int, optional
            The bits of security for the cryptographic context (default is 128).
        generate : bool, optional
            Whether to generate a new secret context (default is True).
        """
        super().__init__()
        if generate:
            self._raw_ctx = _bindings.SecretContext(bits_of_security)

    def encrypt(self, plaintext):
        """
        Encrypts a plaintext value using this secret context.

        Parameters
        ----------
        plaintext : object
            The value to encrypt.

        Returns
        -------
        Ciphertext
            The encrypted value as a Ciphertext object.
        """
        raw_cipher = self._raw_ctx.encrypt(plaintext)
        return Ciphertext(raw_cipher, self)

    def decrypt(self, ciphertext):
        """
        Decrypts a ciphertext using this secret context.

        Parameters
        ----------
        ciphertext : Ciphertext
            The Ciphertext object to decrypt.

        Returns
        -------
        object
            The decrypted value.
        """
        if ciphertext._raw_cipher.is_exact():
            return self._raw_ctx.decrypt_int(ciphertext._raw_cipher)
        else:
            return self._raw_ctx.decrypt_float(ciphertext._raw_cipher)

    def into_public(self):
        """
        Converts this secret context into a public context.

        Returns
        -------
        PublicContext
            A new PublicContext object.
        """
        raw_public_context = self._raw_ctx.as_public()
        public_context = PublicContext()
        public_context._raw_ctx = raw_public_context
        return public_context

    @classmethod
    def from_json(cls, ctx_json):
        """
        Deserializes a secret context from a JSON string.

        Parameters
        ----------
        ctx_json : str
            The JSON string representing the secret context.

        Returns
        -------
        SecretContext
            A new SecretContext object.
        """
        return cls._from_raw(_bindings.SecretContext.from_json(ctx_json))

    @classmethod
    def from_bytes(cls, ctx_bytes):
        """
        Deserializes a secret context from byte representation.

        Parameters
        ----------
        ctx_bytes : bytes
            The bytes representing the secret context.

        Returns
        -------
        SecretContext
            A new SecretContext object.
        """
        return cls._from_raw(_bindings.SecretContext.from_bytes(ctx_bytes))

class PublicContext(Context):
    """
    Represents a public cryptographic context, used for encryption.

    A `PublicContext` is generated from a `SecretContext` and allows for
    encryption operations, but not decryption.

    Attributes
    ----------
    _raw_ctx : object
        The raw public context object from the bindings.
    """

    def __init__(self, generate=False):
        """
        Initializes a new public context.

        Parameters
        ----------
        generate : bool, optional
            Whether to generate a new public context (default is False).
        """
        super().__init__()

    def encrypt(self, plaintext):
        """
        Encrypts the provided plaintext values.

        Parameters
        ----------
        plaintext : object
            The value to encrypt.

        Raises
        ------
        Exception
            Raised because public encryption is currently not supported.

        Returns
        -------
        None
        """
        raise Exception("Public encryption is currently not supported")

    def decrypt(self, ciphertext):
        """
        Decrypts the provided ciphertext.

        Raises
        ------
        Exception
            Raised because public decryption is currently not supported.

        Returns
        -------
        None
        """
        raise Exception("Public decryption is currently not supported")

    @classmethod
    def from_json(cls, ctx_json):
        """
        Deserializes a public context from a JSON string.

        Parameters
        ----------
        ctx_json : str
            The JSON string representing the public context.

        Returns
        -------
        PublicContext
            A new PublicContext object.
        """
        return cls._from_raw(_bindings.PublicContext.from_json(ctx_json))

    @classmethod
    def from_bytes(cls, ctx_bytes):
        """
        Deserializes a public context from byte representation.

        Parameters
        ----------
        ctx_bytes : bytes
            The bytes representing the public context.

        Returns
        -------
        PublicContext
            A new PublicContext object.
        """
        return cls._from_raw(_bindings.PublicContext.from_bytes(ctx_bytes))