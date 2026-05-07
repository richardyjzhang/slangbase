import { http } from './http'

export interface TagType {
  id: string
  name: string
  color: string
  created_at: string
}

interface ListResp {
  items: TagType[]
}

export type TagTypePayload = Pick<TagType, 'name' | 'color'>

export const tagTypesApi = {
  list: () => http.get<ListResp>('/tag-types').then((r) => r.items),
  create: (payload: TagTypePayload) => http.post<TagType>('/tag-types', payload),
  update: (id: string, payload: Partial<TagTypePayload>) =>
    http.put<TagType>(`/tag-types/${encodeURIComponent(id)}`, payload),
  remove: (id: string) => http.delete<void>(`/tag-types/${encodeURIComponent(id)}`),
}
