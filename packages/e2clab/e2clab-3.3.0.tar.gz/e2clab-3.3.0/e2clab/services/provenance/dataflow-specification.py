from dfa_lib_python.attribute import Attribute
from dfa_lib_python.attribute_type import AttributeType
from dfa_lib_python.dataflow import Dataflow
from dfa_lib_python.set import Set
from dfa_lib_python.set_type import SetType
from dfa_lib_python.transformation import Transformation

dataflow_tag = "1"
df = Dataflow(dataflow_tag)
# Transformation model training
tf1 = Transformation("model_training")
tf1_input = Set(
    "training_input",
    SetType.INPUT,
    [
        Attribute("kernel_size", AttributeType.NUMERIC),
        Attribute("num_kernels", AttributeType.NUMERIC),
        Attribute("length_of_strides", AttributeType.NUMERIC),
        Attribute("pooling_size", AttributeType.NUMERIC),
    ],
)
tf1_output = Set(
    "training_output",
    SetType.OUTPUT,
    [
        Attribute("accuracy", AttributeType.NUMERIC),
        Attribute("training_time", AttributeType.NUMERIC),
    ],
)
tf1.set_sets([tf1_input, tf1_output])
df.add_transformation(tf1)
df.save()
