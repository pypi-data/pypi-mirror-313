import inspect

import tensorflow as tf

from kdp.custom_layers import (
    CastToFloat32Layer,
    DateEncodingLayer,
    DateParsingLayer,
    SeasonLayer,
    TextPreprocessingLayer,
    TransformerBlock,
)


class PreprocessorLayerFactory:
    @staticmethod
    def create_layer(layer_class: str | object, name: str = None, **kwargs) -> tf.keras.layers.Layer:
        """Create a layer using the layer class name, automatically filtering kwargs based on the layer class.

        Args:
            layer_class (str | Class Object): The name of the layer class to be created
                (e.g., 'Normalization', 'Rescaling') or the class object itself.
            name (str): The name of the layer. Optional.
            **kwargs: Additional keyword arguments to pass to the layer constructor.

        Returns:
            An instance of the specified layer class.
        """
        # Dynamically get the layer class from TensorFlow Keras layers
        if isinstance(layer_class, str):
            name = name or layer_class.lower()
            layer_class = getattr(tf.keras.layers, layer_class)

        # Get the signature of the layer class constructor
        constructor_params = inspect.signature(layer_class.__init__).parameters

        # Filter kwargs to only include those that the constructor can accept
        filtered_kwargs = {key: value for key, value in kwargs.items() if key in constructor_params}

        # Add the 'name' argument if provided else default the class name lowercase option
        if name:
            filtered_kwargs["name"] = name

        # Create an instance of the layer class with the filtered kwargs
        return layer_class(**filtered_kwargs)

    @staticmethod
    def text_preprocessing_layer(name: str = "text_preprocessing", **kwargs: dict) -> tf.keras.layers.Layer:
        """Create a TextPreprocessingLayer layer.

        Args:
            name: The name of the layer.
            **kwargs: Additional keyword arguments to pass to the layer constructor.

        Returns:
            An instance of the TextPreprocessingLayer layer.
        """
        return PreprocessorLayerFactory.create_layer(
            layer_class=TextPreprocessingLayer,
            name=name,
            **kwargs,
        )

    @staticmethod
    def cast_to_float32_layer(name: str = "cast_to_float32", **kwargs: dict) -> tf.keras.layers.Layer:
        """Create a CastToFloat32Layer layer.

        Args:
            name: The name of the layer.
            **kwargs: Additional keyword arguments to pass to the layer constructor.

        Returns:
            An instance of the CastToFloat32Layer layer.
        """
        return PreprocessorLayerFactory.create_layer(
            layer_class=CastToFloat32Layer,
            name=name,
            **kwargs,
        )

    @staticmethod
    def date_parsing_layer(name: str = "date_parsing_layer", **kwargs: dict) -> tf.keras.layers.Layer:
        """Create a DateParsingLayer layer.

        Args:
            name: The name of the layer.
            **kwargs: Additional keyword arguments to pass to the layer constructor.

        Returns:
            An instance of the DateParsingLayer layer.
        """
        return PreprocessorLayerFactory.create_layer(
            layer_class=DateParsingLayer,
            name=name,
            **kwargs,
        )

    @staticmethod
    def date_encoding_layer(name: str = "date_encoding_layer", **kwargs: dict) -> tf.keras.layers.Layer:
        """Create a DateEncodingLayer layer.

        Args:
            name: The name of the layer.
            **kwargs: Additional keyword arguments to pass to the layer constructor.

        Returns:
            An instance of the DateEncodingLayer layer.
        """
        return PreprocessorLayerFactory.create_layer(
            layer_class=DateEncodingLayer,
            name=name,
            **kwargs,
        )

    @staticmethod
    def date_season_layer(name: str = "date_season_layer", **kwargs: dict) -> tf.keras.layers.Layer:
        """Create a SeasonLayer layer.

        Args:
            name: The name of the layer.
            **kwargs: Additional keyword arguments to pass to the layer constructor.

        Returns:
            An instance of the SeasonLayer layer.
        """
        return PreprocessorLayerFactory.create_layer(
            layer_class=SeasonLayer,
            name=name,
            **kwargs,
        )

    @staticmethod
    def transformer_block_layer(name: str = "transformer", **kwargs: dict) -> tf.keras.layers.Layer:
        """Create a TransformerBlock layer.

        Args:
            name: The name of the layer.
            **kwargs: Additional keyword arguments to pass to the layer constructor.

        Returns:
            An instance of the TransformerBlock layer.
        """
        return PreprocessorLayerFactory.create_layer(
            layer_class=TransformerBlock,
            name=name,
            **kwargs,
        )
