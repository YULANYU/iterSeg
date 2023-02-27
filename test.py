import vtk
import nibabel as nib

# 璇诲彇Nifti鏂囦欢
filename = "lung_002.nii"
nifti = nib.load(filename)

# 鑾峰彇Nifti鏁版嵁鍜屽厓鏁版嵁
data = nifti.get_fdata()
dimensions = data.shape
spacing = nifti.header.get_zooms()

# 杞崲鏁版嵁涓篤TK鏍煎紡
imageData = vtk.vtkImageData()
imageData.SetDimensions(dimensions)
imageData.SetSpacing(spacing)
imageData.AllocateScalars(vtk.VTK_FLOAT, 1)
for z in range(dimensions[2]):
    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            imageData.SetScalarComponentFromFloat(x, y, z, 0, data[x, y, z])

# 鍒涘缓VTK娓叉煋鍣ㄥ拰绐楀彛
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

# 鍒涘缓VTK浜や簰鍣�
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

# 鍒涘缓VTK浣撴覆鏌撳櫒鍜屼綋鏄犲皠鍣�
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
volumeMapper.SetInputData(imageData)
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.ShadeOn()
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# 灏嗕綋娣诲姞鍒版覆鏌撳櫒涓�
renderer.AddViewProp(volume)

# 璁剧疆鐩告満浣嶇疆
camera = renderer.GetActiveCamera()
camera.SetPosition(dimensions[0], dimensions[1], dimensions[2])
camera.SetFocalPoint(0, 0, 0)

# 寮�濮嬫覆鏌撳拰浜や簰
renderWindow.Render()
interactor.Start()
