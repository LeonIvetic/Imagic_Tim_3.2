import { createContext, useContext } from 'react'

export const DataContext = createContext(null)

// Komponente pristupaju podacima samo preko useData() (vidi DataProvider.jsx).
export function useData() {
  const data = useContext(DataContext)
  if (data === null) {
    throw new Error('useData mora biti unutar <DataProvider>')
  }
  return data
}
