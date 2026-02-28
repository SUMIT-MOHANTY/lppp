import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface AppState {
  notifications: Notification[]
  addNotification: (notification: Omit<Notification, 'id'>) => void
  removeNotification: (id: string) => void
  isSidebarOpen: boolean
  toggleSidebar: () => void
}

interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        notifications: [],
        addNotification: (notification) => set((state) => ({
          notifications: [...state.notifications, { ...notification, id: crypto.randomUUID() }]
        })),
        removeNotification: (id) => set((state) => ({
          notifications: state.notifications.filter((n) => n.id !== id)
        })),
        isSidebarOpen: true,
        toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen }))
      }),
      { name: 'app-storage' }
    )
  )
)
