from dbt.adapters.maxcompute.connections import MaxComputeConnectionManager  # noqa
from dbt.adapters.maxcompute.connections import MaxComputeCredentials
from dbt.adapters.maxcompute.impl import MaxComputeAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import maxcompute


Plugin = AdapterPlugin(
    adapter=MaxComputeAdapter,
    credentials=MaxComputeCredentials,
    include_path=maxcompute.PACKAGE_PATH,
)
