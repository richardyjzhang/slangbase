import { http } from './http'

export interface Tag {
  id: string
  tag_type_id: string
  name: string
  created_at: string
  tag_type_name: string
  tag_type_color: string
}

interface ListResp {
  items: Tag[]
}

export type TagCreatePayload = Pick<Tag, 'tag_type_id' | 'name'>
export type TagUpdatePayload = Partial<Pick<Tag, 'tag_type_id' | 'name'>>

export const tagsApi = {
  list: (params?: { tag_type_id?: string }) => {
    const q = params?.tag_type_id
      ? `?tag_type_id=${encodeURIComponent(params.tag_type_id)}`
      : ''
    return http.get<ListResp>(`/tags${q}`).then((r) => r.items)
  },
  create: (payload: TagCreatePayload) => http.post<Tag>('/tags', payload),
  update: (id: string, payload: TagUpdatePayload) =>
    http.put<Tag>(`/tags/${encodeURIComponent(id)}`, payload),
  remove: (id: string) => http.delete<void>(`/tags/${encodeURIComponent(id)}`),
}
