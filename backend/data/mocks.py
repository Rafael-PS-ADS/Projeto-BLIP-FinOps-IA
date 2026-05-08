mock_data = [
    {
        "id": "1",
        "recurso": "vm-blip-prd-01",
        "tipo": "VM",
        "cpu_media": "8%",
        "custo_mensal": 1200,
        "economia": 800,
        "problema": "Oversized (Muito grande para o uso)"
    },
    {
        "id": "2",
        "recurso": "disk-orphan-bkp",
        "tipo": "Managed Disk",
        "cpu_media": "N/A",
        "custo_mensal": 350,
        "economia": 350,
        "problema": "Unattached (Disco solto cobrando)"
    },
    {
        "id": "3",
        "recurso": "vm-teste-dev-04",
        "tipo": "VM",
        "cpu_media": "2%",
        "custo_mensal": 400,
        "economia": 400,
        "problema": "Missing Tags (Sem tag de centro de custo)"
    },
    {
        "id": "4",
        "recurso": "vm-data-worker",
        "tipo": "VM",
        "cpu_media": "15%",
        "custo_mensal": 800,
        "economia": 500,
        "problema": "Oversized"
    },
    {
        "id": "5",
        "recurso": "snap-old-2025",
        "tipo": "Snapshot",
        "cpu_media": "N/A",
        "custo_mensal": 150,
        "economia": 150,
        "problema": "Obsoleto (> 90 dias)"
    }
]

def get_mock_resources():
    return mock_data
