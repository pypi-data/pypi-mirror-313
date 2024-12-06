from sonusai.mixture.datatypes import AugmentationRules
from sonusai.mixture.datatypes import AugmentedTarget
from sonusai.mixture.datatypes import AugmentedTargets
from sonusai.mixture.datatypes import TargetFiles


def get_augmented_targets(
    target_files: TargetFiles,
    target_augmentations: AugmentationRules,
    mixups: list[int] | None = None,
) -> AugmentedTargets:
    from .augmentation import get_augmentation_indices_for_mixup
    from .augmentation import get_mixups

    if mixups is None:
        mixups = get_mixups(target_augmentations)

    augmented_targets: AugmentedTargets = []
    for mixup in mixups:
        augmentation_indices = get_augmentation_indices_for_mixup(target_augmentations, mixup)
        for target_index in range(len(target_files)):
            for augmentation_index in augmentation_indices:
                augmented_targets.append(
                    AugmentedTarget(
                        target_id=target_index,
                        target_augmentation_id=augmentation_index,
                    )
                )

    return augmented_targets


def get_class_index_for_augmented_target(augmented_target: AugmentedTarget, targets: TargetFiles) -> list[int]:
    return targets[augmented_target.target_id].class_indices


def get_mixup_for_augmented_target(augmented_target: AugmentedTarget, augmentations: AugmentationRules) -> int:
    return augmentations[augmented_target.target_augmentation_id].mixup


def get_target_ids_for_class_index(targets: TargetFiles, class_index: int, allow_multiple: bool = False) -> list[int]:
    """Get a list of target indices containing the given class index.

    If allow_multiple is True, then include targets that contain multiple class indices.
    """
    target_indices = set()
    for target_index, target in enumerate(targets):
        indices = target.class_indices
        if len(indices) == 1 or allow_multiple:
            for index in indices:
                if index == class_index + 1:
                    target_indices.add(target_index)

    return sorted(target_indices)


def get_augmented_target_ids_for_class_index(
    augmented_targets: AugmentedTargets,
    targets: TargetFiles,
    augmentations: AugmentationRules,
    class_index: int,
    mixup: int,
    allow_multiple: bool = False,
) -> list[int]:
    """Get a list of augmented target indices containing the given class index.

    If allow_multiple is True, then include targets that contain multiple class indices.
    """
    augmented_target_ids = set()
    for augmented_target_id, augmented_target in enumerate(augmented_targets):
        if get_mixup_for_augmented_target(augmented_target=augmented_target, augmentations=augmentations) == mixup:
            indices = get_class_index_for_augmented_target(augmented_target=augmented_target, targets=targets)
            if len(indices) == 1 or allow_multiple:
                for index in indices:
                    if index == class_index + 1:
                        augmented_target_ids.add(augmented_target_id)

    return sorted(augmented_target_ids)


def get_augmented_target_ids_by_class(
    augmented_targets: AugmentedTargets,
    targets: TargetFiles,
    target_augmentations: AugmentationRules,
    mixup: int,
    num_classes: int,
) -> list[list[int]]:
    indices = []
    for idx in range(num_classes):
        indices.append(
            get_augmented_target_ids_for_class_index(
                augmented_targets=augmented_targets,
                targets=targets,
                augmentations=target_augmentations,
                class_index=idx,
                mixup=mixup,
            )
        )
    return indices


def get_target_augmentations_for_mixup(target_augmentations: AugmentationRules, mixup: int) -> AugmentationRules:
    """Get target augmentations for a given mixup value

    :param target_augmentations: List of target augmentation rules
    :param mixup: Mixup value of interest
    :return: Target augmentations
    """
    return [target_augmentation for target_augmentation in target_augmentations if target_augmentation.mixup == mixup]


def get_augmented_target_ids_for_mixup(
    augmented_targets: AugmentedTargets,
    targets: TargetFiles,
    target_augmentations: AugmentationRules,
    mixup: int,
    num_classes: int,
) -> list[list[int]]:
    from collections import deque
    from random import shuffle

    mixup_indices = []

    if mixup == 1:
        for index, augmented_target in enumerate(augmented_targets):
            if (
                get_mixup_for_augmented_target(
                    augmented_target=augmented_target,
                    augmentations=target_augmentations,
                )
                == 1
            ):
                mixup_indices.append([index])
        return mixup_indices

    augmented_target_ids_by_class = get_augmented_target_ids_by_class(
        augmented_targets=augmented_targets,
        targets=targets,
        target_augmentations=target_augmentations,
        mixup=mixup,
        num_classes=num_classes,
    )

    if mixup > num_classes:
        raise ValueError(f"Specified mixup, {mixup}, is greater than the number of classes, {num_classes}")

    de: deque[int] = deque()

    # Keep looping until not enough targets remain for mixup
    while sum([1 for x in augmented_target_ids_by_class if x]) >= mixup:
        # Need more class indices?
        if len(de) < mixup:
            # Only choose classes that still have data
            counts = [len(item) for item in augmented_target_ids_by_class]
            # Need to subtract out indices already in the deque
            for idx in de:
                counts[idx] -= 1
            indices = [idx for idx, val in enumerate(counts) if val > 0]
            shuffle(indices)
            # Keep shuffling if the deque is not empty and the first new index matches the last item
            # (so that a class does not appear twice in a mixup)
            while de and indices[0] == de[-1]:
                shuffle(indices)
            for index in indices:
                de.append(index)

        class_indices = [de.popleft() for _ in range(mixup)]

        target_indices = []
        for class_index in class_indices:
            target_indices.append(augmented_target_ids_by_class[class_index].pop())

        mixup_indices.append(target_indices)

    return mixup_indices
