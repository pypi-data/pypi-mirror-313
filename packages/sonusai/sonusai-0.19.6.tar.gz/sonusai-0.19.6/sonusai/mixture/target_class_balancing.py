from sonusai.mixture.datatypes import AugmentationRule
from sonusai.mixture.datatypes import AugmentationRules
from sonusai.mixture.datatypes import AugmentedTargets
from sonusai.mixture.datatypes import TargetFile
from sonusai.mixture.datatypes import TargetFiles


def balance_targets(
    augmented_targets: AugmentedTargets,
    targets: TargetFiles,
    target_augmentations: AugmentationRules,
    class_balancing_augmentation: AugmentationRule,
    num_classes: int,
    num_ir: int,
    mixups: list[int] | None = None,
) -> tuple[AugmentedTargets, AugmentationRules]:
    import math

    from .augmentation import get_mixups
    from .datatypes import AugmentedTarget
    from .targets import get_augmented_target_ids_by_class

    first_cba_id = len(target_augmentations)

    if mixups is None:
        mixups = get_mixups(target_augmentations)

    for mixup in mixups:
        if mixup == 1:
            continue

        augmented_target_indices_by_class = get_augmented_target_ids_by_class(
            augmented_targets=augmented_targets,
            targets=targets,
            target_augmentations=target_augmentations,
            mixup=mixup,
            num_classes=num_classes,
        )

        largest = max([len(item) for item in augmented_target_indices_by_class])
        largest = math.ceil(largest / mixup) * mixup
        for at_indices in augmented_target_indices_by_class:
            additional_augmentations_needed = largest - len(at_indices)
            target_ids = sorted({augmented_targets[at_index].target_id for at_index in at_indices})

            tfi_idx = 0
            for _ in range(additional_augmentations_needed):
                target_id = target_ids[tfi_idx]
                tfi_idx = (tfi_idx + 1) % len(target_ids)
                augmentation_index, target_augmentations = _get_unused_balancing_augmentation(
                    augmented_targets=augmented_targets,
                    targets=targets,
                    target_augmentations=target_augmentations,
                    class_balancing_augmentation=class_balancing_augmentation,
                    target_id=target_id,
                    mixup=mixup,
                    num_ir=num_ir,
                    first_cba_id=first_cba_id,
                )
                augmented_target = AugmentedTarget(target_id=target_id, target_augmentation_id=augmentation_index)
                augmented_targets.append(augmented_target)

    return augmented_targets, target_augmentations


def _get_unused_balancing_augmentation(
    augmented_targets: AugmentedTargets,
    targets: TargetFiles,
    target_augmentations: AugmentationRules,
    class_balancing_augmentation: AugmentationRule,
    target_id: int,
    mixup: int,
    num_ir: int,
    first_cba_id: int,
) -> tuple[int, AugmentationRules]:
    """Get an unused balancing augmentation for a given target file index"""
    from dataclasses import asdict

    from .augmentation import get_augmentation_rules

    balancing_augmentations = [item for item in range(len(target_augmentations)) if item >= first_cba_id]
    used_balancing_augmentations = [
        at.target_augmentation_id
        for at in augmented_targets
        if at.target_id == target_id and at.target_augmentation_id in balancing_augmentations
    ]

    augmentation_indices = [
        item
        for item in balancing_augmentations
        if item not in used_balancing_augmentations and target_augmentations[item].mixup == mixup
    ]
    if len(augmentation_indices) > 0:
        return augmentation_indices[0], target_augmentations

    class_balancing_augmentation = get_class_balancing_augmentation(
        target=targets[target_id], default_cba=class_balancing_augmentation
    )
    new_augmentation = get_augmentation_rules(rules=asdict(class_balancing_augmentation), num_ir=num_ir)[0]
    new_augmentation.mixup = mixup
    target_augmentations.append(new_augmentation)
    return len(target_augmentations) - 1, target_augmentations


def get_class_balancing_augmentation(target: TargetFile, default_cba: AugmentationRule) -> AugmentationRule:
    """Get the class balancing augmentation rule for the given target"""
    if target.class_balancing_augmentation is not None:
        return target.class_balancing_augmentation
    return default_cba
