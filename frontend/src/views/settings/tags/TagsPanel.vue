<script setup lang="ts">
import { computed, h, onMounted, reactive, ref, watch } from 'vue'
import {
  NAlert,
  NButton,
  NDataTable,
  NEmpty,
  NForm,
  NFormItem,
  NIcon,
  NInput,
  NModal,
  NPopconfirm,
  NSelect,
  NSpace,
  NSpin,
  useMessage,
  type DataTableColumns,
  type FormInst,
  type FormRules,
  type SelectOption,
} from 'naive-ui'
import { AddOutline, CreateOutline, RefreshOutline, TrashOutline } from '@vicons/ionicons5'
import ColoredTag from '@/components/ColoredTag.vue'
import { tagTypesApi, type TagType } from '@/api/tagTypes'
import { tagsApi, type Tag } from '@/api/tags'
import { ApiError } from '@/api/http'

const message = useMessage()

const tagTypes = ref<TagType[]>([])
const items = ref<Tag[]>([])
const loading = ref(false)
const typesLoading = ref(false)

const filterTypeId = ref<string | null>(null)

const modalVisible = ref(false)
const submitting = ref(false)
const editingId = ref<string | null>(null)
const formRef = ref<FormInst | null>(null)
const formValue = reactive<{ tag_type_id: string | null; name: string }>({
  tag_type_id: null,
  name: '',
})

const isEdit = computed(() => editingId.value !== null)

const typeOptions = computed(() =>
  tagTypes.value.map((t) => ({ label: t.name, value: t.id, color: t.color })),
)

function resolveOptionLabel(option: SelectOption): string {
  if (typeof option.label === 'string') return option.label
  return String(option.value ?? '')
}

function optionHexColor(option: SelectOption): string {
  const c = (option as SelectOption & { color?: string }).color
  return typeof c === 'string' && /^#[0-9a-fA-F]{6}$/.test(c) ? c : '#64748b'
}

function renderTypeLabel(option: SelectOption) {
  return h(ColoredTag, {
    label: resolveOptionLabel(option),
    color: optionHexColor(option),
  })
}

const rules: FormRules = {
  tag_type_id: [
    {
      required: true,
      validator: (_r, value: string | null) => value !== null && value !== '',
      message: '请选择标签类型',
      trigger: ['change', 'blur'],
    },
  ],
  name: [
    { required: true, message: '请输入名称', trigger: ['input', 'blur'] },
    {
      validator: (_r, value: string) => !!value && value.trim().length > 0 && value.length <= 64,
      message: '名称不能为空，且不超过 64 字符',
      trigger: ['input', 'blur'],
    },
  ],
}

async function fetchTagTypes() {
  typesLoading.value = true
  try {
    tagTypes.value = await tagTypesApi.list()
  } catch (e) {
    message.error(e instanceof ApiError ? e.message : '加载标签类型失败')
  } finally {
    typesLoading.value = false
  }
}

async function fetchList() {
  loading.value = true
  try {
    const tid = filterTypeId.value
    items.value = await tagsApi.list(tid ? { tag_type_id: tid } : undefined)
  } catch (e) {
    message.error(e instanceof ApiError ? e.message : '加载标签失败')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  formValue.tag_type_id = filterTypeId.value ?? tagTypes.value[0]?.id ?? null
  formValue.name = ''
  modalVisible.value = true
}

function openEdit(row: Tag) {
  editingId.value = row.id
  formValue.tag_type_id = row.tag_type_id
  formValue.name = row.name
  modalVisible.value = true
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }
  if (formValue.tag_type_id === null) {
    message.warning('请选择标签类型')
    return
  }
  submitting.value = true
  try {
    const payload = { tag_type_id: formValue.tag_type_id, name: formValue.name.trim() }
    if (isEdit.value && editingId.value) {
      await tagsApi.update(editingId.value, payload)
      message.success('已保存')
    } else {
      await tagsApi.create(payload)
      message.success('已创建')
    }
    modalVisible.value = false
    await fetchList()
  } catch (e) {
    message.error(e instanceof ApiError ? e.message : '保存失败')
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row: Tag) {
  try {
    await tagsApi.remove(row.id)
    message.success('已删除')
    await fetchList()
  } catch (e) {
    message.error(e instanceof ApiError ? e.message : '删除失败')
  }
}

const columns = computed<DataTableColumns<Tag>>(() => [
  {
    title: '名称',
    key: 'name',
    minWidth: 160,
    render: (row) => h(ColoredTag, { label: row.name, color: row.tag_type_color }),
  },
  {
    title: '所属类型',
    key: 'tag_type_name',
    width: 200,
    ellipsis: { tooltip: true },
    render: (row) =>
      h('span', { class: 'text-gray-900' }, row.tag_type_name),
  },
  {
    title: '操作',
    key: 'actions',
    width: 168,
    fixed: 'right',
    titleAlign: 'left',
    align: 'right',
    render: (row) =>
      h(NSpace, { size: 4, wrap: false, justify: 'end' }, () => [
        h(
          NButton,
          { size: 'small', text: true, type: 'primary', onClick: () => openEdit(row) },
          {
            icon: () => h(NIcon, null, { default: () => h(CreateOutline) }),
            default: () => '编辑',
          },
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete(row),
            positiveText: '删除',
            negativeText: '取消',
          },
          {
            trigger: () =>
              h(
                NButton,
                { size: 'small', text: true, type: 'error' },
                {
                  icon: () => h(NIcon, null, { default: () => h(TrashOutline) }),
                  default: () => '删除',
                },
              ),
            default: () => `确定删除标签「${row.name}」吗？`,
          },
        ),
      ]),
  },
])

const hasTypes = computed(() => tagTypes.value.length > 0)

watch(filterTypeId, () => {
  void fetchList()
})

onMounted(async () => {
  await fetchTagTypes()
  await fetchList()
})
</script>

<template>
  <div class="flex flex-col gap-3">
    <div class="flex flex-wrap items-center justify-between gap-2">
      <span class="text-sm text-gray-500">
        每个标签从属于一种类型；同一类型下名称不可重复。
      </span>
      <n-space>
        <n-select
          v-model:value="filterTypeId"
          clearable
          placeholder="按类型筛选"
          class="min-w-[200px]"
          :options="typeOptions"
          :loading="typesLoading"
          :render-label="renderTypeLabel"
        />
        <n-button :loading="loading" @click="fetchList">
          <template #icon>
            <n-icon><RefreshOutline /></n-icon>
          </template>
          刷新
        </n-button>
        <n-button type="primary" :disabled="!hasTypes" @click="openCreate">
          <template #icon>
            <n-icon><AddOutline /></n-icon>
          </template>
          新建标签
        </n-button>
      </n-space>
    </div>

    <n-alert v-if="!hasTypes && !typesLoading" type="warning" class="text-sm">
      还没有标签类型，请先在「标签类型」页签中创建。
    </n-alert>

    <n-spin :show="loading">
      <n-data-table
        :columns="columns"
        :data="items"
        :bordered="false"
        :single-line="false"
        size="small"
        :row-key="(row: Tag) => row.id"
      >
        <template #empty>
          <n-empty :description="hasTypes ? '还没有标签' : '暂无可选类型'" />
        </template>
      </n-data-table>
    </n-spin>

    <n-modal
      v-model:show="modalVisible"
      preset="card"
      :title="isEdit ? '编辑标签' : '新建标签'"
      style="width: 420px"
      :mask-closable="false"
    >
      <n-form
        ref="formRef"
        :model="formValue"
        :rules="rules"
        label-placement="left"
        label-width="72"
        require-mark-placement="right-hanging"
      >
        <n-form-item label="类型" path="tag_type_id">
          <n-select
            v-model:value="formValue.tag_type_id"
            placeholder="选择标签类型"
            to="body"
            :options="typeOptions"
            :loading="typesLoading"
            :render-label="renderTypeLabel"
          />
        </n-form-item>
        <n-form-item label="名称" path="name">
          <n-input
            v-model:value="formValue.name"
            placeholder="标签名称"
            maxlength="64"
            show-count
          />
        </n-form-item>
      </n-form>
      <template #footer>
        <div class="flex justify-end gap-2">
          <n-button @click="modalVisible = false">取消</n-button>
          <n-button type="primary" :loading="submitting" @click="handleSubmit">
            {{ isEdit ? '保存' : '创建' }}
          </n-button>
        </div>
      </template>
    </n-modal>
  </div>
</template>
