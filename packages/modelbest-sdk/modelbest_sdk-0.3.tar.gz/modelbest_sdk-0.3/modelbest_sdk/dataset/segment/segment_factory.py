from modelbest_sdk.dataset.segment.conditionl_fixed_length_segment import ConditionalFixedLengthSegment
from modelbest_sdk.dataset.segment.fixed_length_segment import FixedLengthSegment
from modelbest_sdk.dataset.segment.no_segment import NoSegment
from modelbest_sdk.dataset.segment.rolling_truncate_segment import RollingTruncateSegment

NO_SEGMENT = 'no_segment'
FIXED_LENGTH_SEGMENT = 'fixed_length_segment'
CONDITIONAL_FIXED_LENGTH_SEGMENT = 'conditional_fixed_length_segment'
ROLLING_TRUNCATE_SEGMENT = 'rolling_truncate_segment'
class SegmentFactory:
    @staticmethod
    def create_segment(segment_type, max_len: int, drop_last=False, **kwargs):
        segment_class = SegmentRegistry.get_segment(segment_type)
        return segment_class(max_len, drop_last, **kwargs)

class SegmentRegistry:
    _registry = {}

    @classmethod
    def register_segment(cls, key, segment_class):
        if key in cls._registry:
            raise ValueError(f"Segment type '{key}' is already registered.")
        cls._registry[key] = segment_class

    @classmethod
    def get_segment(cls, key):
        if key not in cls._registry:
            raise ValueError(f"Unsupported segment type: {key}")
        return cls._registry[key]

SegmentRegistry.register_segment(NO_SEGMENT, NoSegment)
SegmentRegistry.register_segment(FIXED_LENGTH_SEGMENT, FixedLengthSegment)
SegmentRegistry.register_segment(CONDITIONAL_FIXED_LENGTH_SEGMENT, ConditionalFixedLengthSegment)
SegmentRegistry.register_segment(ROLLING_TRUNCATE_SEGMENT, RollingTruncateSegment)