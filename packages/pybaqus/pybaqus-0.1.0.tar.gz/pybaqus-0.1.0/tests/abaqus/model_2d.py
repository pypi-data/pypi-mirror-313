import os

from abaqus import *
import assembly
import datum
import interaction
import job
import load
import material
import mesh
import part
import partition
import regionToolset
import section
import sketch
import step
from abaqus import backwardCompatibility, mdb, monitorManager, session
from abaqusConstants import *
from jobMessage import *
from odbAccess import Odb

# Set backward compatibility
backwardCompatibility.setValues(includeDeprecated=False, reportDeprecated=True)


def get_ascii_job(job_obj):
    """Configure Job to save results in the ASCII format (*.fil).

    Parameters
    ----------
    job_obj : TODO

    """
    job_obj.writeInput(consistencyChecking=False)

    input_lines = (
        "*FILE FORMAT, ASCII\n"
        + "*EL FILE\n"
        + "S, E, COORD\n"
        + "*NODE FILE\n"
        + "COORD, U\n"
    )

    # Open *inp file
    file_name = job_obj.name + ".inp"

    with open(file_name, "r") as inp_file:
        lines = inp_file.readlines()

    with open(file_name, "w") as inp_file:
        for l in lines:
            if l == "*End Step\n":
                inp_file.writelines(input_lines)
                inp_file.write(l)
            else:
                inp_file.write(l)

    job_ascii = mdb.JobFromInputFile(
        name=job_obj.name,
        inputFileName=job_obj.name + ".inp",
        type=ANALYSIS,
        memory=90,
        memoryUnits=PERCENTAGE,
        getMemoryFromAnalysis=True,
        explicitPrecision=SINGLE,
        nodalOutputPrecision=SINGLE,
        userSubroutine=job_obj.userSubroutine,
        scratch=job_obj.scratch,
        multiprocessingMode=DEFAULT,
        numCpus=job_obj.numCpus,
        numDomains=job_obj.numDomains,
    )

    return job_ascii


# Define some parameters
x0 = 0.1
y0 = 0.2
w = 12.8
h = 10.3

# Model
model = mdb.Model(name="test")
# Viewport
viewp = session.Viewport(name="test", origin=(20, 0), width=450, height=170)

sketch_test = model.ConstrainedSketch(name="test", sheetSize=200.0)
sketch_test.rectangle(point1=(x0, y0), point2=(x0 + w, y0 + h))

test_part = model.Part(name="test", dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
test_part.BaseShell(sketch=sketch_test)

props = (1000, 0.3)

test_mat = model.Material(name="test-material")
test_mat.Elastic(table=(props,), type=ISOTROPIC)

test_sec = model.HomogeneousSolidSection(
    name="test-section", material=test_mat.name, thickness=1
)
# Create sets to assign section to
set_faces = test_part.Set(faces=test_part.faces[:], name="set-test_part")

test_part.SectionAssignment(
    region=set_faces, sectionName="test-section", thicknessAssignment=FROM_SECTION
)

asmbly = model.rootAssembly
inst = asmbly.Instance(name="name", part=test_part, dependent=False)

step_test = model.StaticStep(
    name="test-step",
    previous="Initial",
    nlgeom=False,
    timeIncrementationMethod=AUTOMATIC,
    initialInc=1,
    maxInc=1.0,
    maxNumInc=10,
)

# Load definition
vertex_load = inst.vertices.findAt(((x0 + w, y0 + h, 0),))
region_shell = regionToolset.Region(vertices=vertex_load)
model.ConcentratedForce(
    name="test-load", createStepName=step_test.name, region=region_shell, cf2=1
)

# Boundary conditions
vert_1 = inst.vertices.findAt(((x0, y0, 0),))
vert_2 = inst.vertices.findAt(((x0 + w, y0, 0),))
region_bottom_1 = regionToolset.Region(vertices=vert_1)
region_bottom_2 = regionToolset.Region(vertices=vert_2)
model.DisplacementBC(
    name="test-bc-1", createStepName="Initial", region=region_bottom_1, u1=0, u2=0
)
model.DisplacementBC(
    name="test-bc-2", createStepName="Initial", region=region_bottom_2, u2=0
)

# Mesh the model
mesh_region = (inst.faces,)
elemType_1 = mesh.ElemType(elemCode=CPS4R, elemLibrary=STANDARD)

asmbly.setElementType(regions=mesh_region, elemTypes=(elemType_1,))
asmbly.seedPartInstance(regions=(inst,), size=(w))
asmbly.generateMesh(regions=(inst,))

job_test = mdb.Job(
    name="test",
    model=model.name,
    description="some description",
    numCpus=1,
    numDomains=1,
)

get_ascii_job(job_obj=job_test)
