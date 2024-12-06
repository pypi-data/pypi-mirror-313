import sys

from robot_image.highlight_image import highlight_section, find_target_position

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("参数错误", file=sys.stderr)
    else:
        pos = find_target_position(sys.argv[1], True, float(sys.argv[2]), sys.argv[3])
        if pos is not None:
            highlight_section(
                (int(pos[2] - pos[0]), int(pos[3] - pos[1]), int(pos[0]), int(pos[1])),
                duration=3,
            )
            print("OK")
        else:
            print("None")
