<script setup lang="ts">
import { computed, h, onMounted, reactive, ref } from 'vue'
import {
  NButton,
  NColorPicker,
  NDataTable,
  NEmpty,
  NForm,
  NFormItem,
  NIcon,
  NInput,
  NModal,
  NPopconfirm,
  NSpace,
  NSpin,
  useMessage,
  type DataTableColumns,
  type FormInst,
  type FormRules,
} from 'naive-ui'
import { AddOutline, CreateOutline, RefreshOutline, TrashOutline } from '@vicons/ionicons5'
import { tagTypesApi, type TagType } from '@/api/tagTypes'
import { ApiError } from '@/api/http'

const message = useMessage()

const items = ref<TagType[]>([])
const loading = ref(false)

const modalVisible = ref(false)
const submitting = ref(false)
// editingId 区分新建 / 编辑：null = 新建；否则是被编辑那条的 UUID
const editingId = ref<string | null>(null)
const formRef = ref<FormInst | null>(null)
const formValue = reactive<{ name: string; color: string }>({
  name: '',
  color: '#3b82f6',
})

const isEdit = computed(() => editingId.value !== null)

const rules: FormRules = {
  name: [
    { required: true, message: '请输入名称', trigger: ['input', 'blur'] },
    {
      validator: (_r, value: string) => !!value && value.trim().length > 0 && value.length <= 64,
      message: '名称不能为空，且不超过 64 字符',
      trigger: ['input', 'blur'],
    },
  ],
  color: [
    { required: true, message: '请选择颜色', trigger: ['change', 'blur'] },
    {
      validator: (_r, value: string) => /^#[0-9a-fA-F]{6}$/.test(value ?? ''),
      message: '颜色必须是 #RRGGBB 形式',
      trigger: ['change', 'blur'],
    },
  ],
}

async function fetchList() {
  loading.value = true
  try {
    items.value = await tagTypesApi.list()
  } catch (e) {
    message.error(e instanceof ApiError ? e.message : '加载标签类型失败')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  formValue.name = ''
  formValue.color = '#3b82f6'
  modalVisible.value = true
}

function openEdit(row: TagType) {
  editingId.value = row.id
  formValue.name = row.name
  formValue.color = row.color
  modalVisible.value = true
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
  } catch {
    return
  }
  submitting.value = true
  try {
    const payload = { name: formValue.name.trim(), color: formValue.color }
    if (isEdit.value && editingId.value) {
      await tagTypesApi.update(editingId.value, payload)
      message.success('已保存')
    } else {
      await tagTypesApi.create(payload)
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

async function handleDelete(row: TagType) {
  try {
    await tagTypesApi.remove(row.id)
    message.success('已删除')
    await fetchList()
  } catch (e) {
    message.error(e instanceof ApiError ? e.message : '删除失败')
  }
}

const columns = computed<DataTableColumns<TagType>>(() => [
  {
    title: '名称',
    key: 'name',
    width: 240,
    render: (row) =>
      h(
        'span',
        {
          class:
            'inline-flex max-w-full items-center rounded-full px-3 py-0.5 text-sm leading-normal tracking-normal whitespace-nowrap text-white [font-synthesis:none]',
          style: {
            backgroundColor: row.color,
            border: `1px solid ${row.color}`,
          },
        },
        row.name,
      ),
  },
  {
    title: '颜色',
    key: 'color',
    width: 200,
    render: (row) =>
      h('div', { class: 'flex items-center gap-2' }, [
        h('span', {
          class: 'inline-block h-4 w-4 rounded border border-gray-200',
          style: { background: row.color },
        }),
        h('span', { class: 'font-mono text-sm text-gray-600' }, row.color),
      ]),
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
            default: () => `确定删除标签类型「${row.name}」吗？`,
          },
        ),
      ]),
  },
])

onMounted(fetchList)
</script>

<template>
  <div class="flex flex-col gap-3">
    <div class="flex items-center justify-between">
      <span class="text-sm text-gray-500">
        管理标签的分类，例如「领域」「部门」等。每种类型对应一个展示颜色。
      </span>
      <n-space>
        <n-button :loading="loading" @click="fetchList">
          <template #icon>
            <n-icon><RefreshOutline /></n-icon>
          </template>
          刷新
        </n-button>
        <n-button type="primary" @click="openCreate">
          <template #icon>
            <n-icon><AddOutline /></n-icon>
          </template>
          新建标签类型
        </n-button>
      </n-space>
    </div>

    <n-spin :show="loading">
      <n-data-table
        :columns="columns"
        :data="items"
        :bordered="false"
        :single-line="false"
        size="small"
        :row-key="(row: TagType) => row.id"
      >
        <template #empty>
          <n-empty description="还没有标签类型" />
        </template>
      </n-data-table>
    </n-spin>

    <n-modal
      v-model:show="modalVisible"
      preset="card"
      :title="isEdit ? '编辑标签类型' : '新建标签类型'"
      style="width: 420px"
      :mask-closable="false"
    >
      <n-form
        ref="formRef"
        :model="formValue"
        :rules="rules"
        label-placement="left"
        label-width="60"
        require-mark-placement="right-hanging"
      >
        <n-form-item label="名称" path="name">
          <n-input
            v-model:value="formValue.name"
            placeholder="如 领域 / 部门"
            maxlength="64"
            show-count
          />
        </n-form-item>
        <n-form-item label="颜色" path="color">
          <n-color-picker
            v-model:value="formValue.color"
            :show-alpha="false"
            :modes="['hex']"
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
