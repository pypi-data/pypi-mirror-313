from .base import InstructionBase
from ..produce import DefaultProduce


class StorageFlushInstruction(InstructionBase):
    head = '$<'
    produce_cls = DefaultProduce

    def run(self, variables, storage):
        if self.value is None:
            reset = True
        else:
            reset = self.instruction_set.eval_expression(None, self.value, variables)
        return [storage.flush(self.produce_cls.wrapper(self.key), reset)]
