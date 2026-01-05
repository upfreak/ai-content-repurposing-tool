import { create } from 'zustand'

export const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: false,
  
  setUser: (user) => set({ user, isAuthenticated: !!user }),
  
  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    set({ user: null, isAuthenticated: false })
  },
  
  initAuth: () => {
    const token = localStorage.getItem('access_token')
    if (token) {
      set({ isAuthenticated: true })
    }
  },
}))

export const useContentStore = create((set) => ({
  contents: [],
  selectedContent: null,
  generations: {},
  
  setContents: (contents) => set({ contents }),
  
  addContent: (content) => set((state) => ({
    contents: [content, ...state.contents],
  })),
  
  setSelectedContent: (content) => set({ selectedContent: content }),
  
  setGenerations: (contentId, generations) =>
    set((state) => ({
      generations: { ...state.generations, [contentId]: generations },
    })),
  
  addGeneration: (contentId, generation) =>
    set((state) => ({
      generations: {
        ...state.generations,
        [contentId]: [...(state.generations[contentId] || []), generation],
      },
    })),
}))
