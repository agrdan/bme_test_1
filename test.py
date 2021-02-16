from controller.BMEController import BMEController


entityList = BMEController().getAll()
dtoList = []

for e in entityList:
    dto = BMEController.entityToExportDto(e)
    dtoList.append(dto)


for d in dtoList:
    print(d)

