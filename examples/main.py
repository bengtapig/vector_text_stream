import anki_vector
from vector_text_stream.util import show_text


def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        # If necessary, move Vector's Head and Lift to make it easy to see his face
        robot.behavior.set_head_angle(anki_vector.util.degrees(25.0))
        robot.behavior.set_lift_height(0.0)

        # Show current track info on Vector's face
        # show_text(robot, 'Hello World! This is a test script to show '
        # 'a relatively long string on the screen of Vector.')
        show_text(robot, "Hello World!")


if __name__ == "__main__":
    main()
