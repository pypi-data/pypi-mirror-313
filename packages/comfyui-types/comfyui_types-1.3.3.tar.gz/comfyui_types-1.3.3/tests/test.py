"""Test ComfyUI node."""

from comfyui_types import ComfyUINode, IntegerOutput, StringInput


class TestNode(ComfyUINode):
    """Test node."""

    function: str = 'execute'
    display_name: str = ''
    output_node: bool = False

    var1 = StringInput(default='hello', display_name='Var 1')
    var2 = StringInput(default='world', display_name='Var 2')
    var3 = StringInput(required=False, display_name='Var 3')

    output = IntegerOutput(display_name='Output')


def main() -> None:
    t = TestNode()

    print(t.FUNCTION)
    print(t.CATEGORY)
    print(t.DISPLAY_NAME)
    print(t.OUTPUT_NODE)
    print(t.INPUT_TYPES())

if __name__ == '__main__':
    main()
