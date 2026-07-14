import api from './client';

export async function getCollectionReport() {
  const { data } = await api.get('/reports/collection');
  return data as { total_collection: number };
}

export async function getPendingFeesReport() {
  const { data } = await api.get('/reports/pending-fees');
  return data as { pending_fees: number };
}
