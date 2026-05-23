"""MCP Server - Mock API集成服务器"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn

from mock_erp import MockERP
from mock_wms import MockWMS
from mock_tms import MockTMS

app = FastAPI(title="Supply Chain MCP Server")

erp = MockERP()
wms = MockWMS()
tms = MockTMS()

class InventoryQuery(BaseModel):
    sku: str
    quantity: int
    warehouses: Optional[List[str]] = None

class RoutingCalculate(BaseModel):
    source: str
    destination: str
    weight: float
    transport_type: str = "公路"

class ShipmentCreate(BaseModel):
    order_id: str
    source: str
    destination: str
    weight: float

@app.post("/api/erp/order/get")
async def get_order(order_id: str):
    return erp.get_order(order_id)

@app.post("/api/erp/order/update")
async def update_order(order_id: str, status: str):
    return erp.update_order_status(order_id, status)

@app.post("/api/inventory/query")
async def query_inventory(query: InventoryQuery):
    return wms.query_inventory(query.sku, query.warehouses)

@app.post("/api/inventory/allocate")
async def allocate_inventory(sku: str, quantity: int, warehouse: str):
    return wms.allocate(sku, quantity, warehouse)

@app.post("/api/routing/calculate")
async def calculate_routing(params: RoutingCalculate):
    return tms.calculate_route(params.source, params.destination, params.weight)

@app.post("/api/shipment/create")
async def create_shipment(data: ShipmentCreate):
    return tms.create_shipment(data.dict())

@app.get("/api/shipment/track/{shipment_id}")
async def track_shipment(shipment_id: str):
    return tms.track(shipment_id)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "supply-chain-mcp"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)