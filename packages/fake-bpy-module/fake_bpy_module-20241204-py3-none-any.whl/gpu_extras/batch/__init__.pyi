import typing
import collections.abc
import typing_extensions
import gpu.types

def batch_for_shader(
    shader: gpu.types.GPUShader, type: str, content: gpu.types.Buffer, *, indices=None
) -> gpu.types.GPUBatch:
    """Return a batch already configured and compatible with the shader.

        :param shader: shader for which a compatible format will be computed.
        :type shader: gpu.types.GPUShader
        :param type: "'POINTS', 'LINES', 'TRIS' or 'LINES_ADJ'".
        :type type: str
        :param content: Maps the name of the shader attribute with the data to fill the vertex buffer.
    For the dictionary values see documentation for `gpu.types.GPUVertBuf.attr_fill` data argument.
        :type content: gpu.types.Buffer
        :return: compatible batch
        :rtype: gpu.types.GPUBatch
    """
