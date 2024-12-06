depends = ('ITKPyBase', 'ITKMesh', 'ITKIOMeshBase', 'ITKCommon', )
templates = (  ('MZ3MeshIO', 'itk::MZ3MeshIO', 'itkMZ3MeshIO', True),
  ('MZ3MeshIOFactory', 'itk::MZ3MeshIOFactory', 'itkMZ3MeshIOFactory', True),
)
factories = (("MeshIO","MZ3"),)
