# frontend/static/js/database.js
class DatabaseManager {
    constructor(databaseId) {
        this.databaseId = databaseId;
        this.currentView = 'table';
        this.records = [];
        this.schema = {};
        this.filters = [];
        this.sorts = [];

        this.initializeEventListeners();
        this.loadData();
    }

    async initializeEventListeners() {
        // 데이터베이스 제목 수정
        document.getElementById('databaseTitle').addEventListener('blur', async (e) => {
            await this.updateDatabase({ name: e.target.textContent });
        });

        // 데이터베이스 설명 수정
        document.getElementById('databaseDescription').addEventListener('blur', async (e) => {
            await this.updateDatabase({ description: e.target.textContent });
        });

        // 뷰 전환 이벤트 처리
        document.querySelectorAll('[data-view]').forEach(button => {
            button.addEventListener('click', () => {
                this.switchView(button.dataset.view);
            });
        });
    }

    async loadData() {
        try {
            // 데이터베이스 정보 로드
            const response = await fetch(`/api/v1/databases/${this.databaseId}`);
            const database = await response.json();

            this.schema = database.schema;
            this.updateDatabaseInfo(database);

            // 레코드 로드
            await this.loadRecords();

        } catch (error) {
            console.error('Error loading database:', error);
            alert('데이터베이스 로드에 실패했습니다.');
        }
    }

    async loadRecords() {
        try {
            const queryParams = new URLSearchParams({
                filters: JSON.stringify(this.filters),
                sorts: JSON.stringify(this.sorts)
            });

            const response = await fetch(
                `/api/v1/databases/${this.databaseId}/records?${queryParams}`
            );
            this.records = await response.json();
            this.renderCurrentView();

        } catch (error) {
            console.error('Error loading records:', error);
            alert('레코드 로드에 실패했습니다.');
        }
    }

    updateDatabaseInfo(database) {
        document.getElementById('databaseTitle').textContent = database.name;
        document.getElementById('databaseDescription').textContent =
            database.description || '설명 추가...';
    }

    async createNewRecord() {
        const modal = document.getElementById('modal');
        const modalContent = document.getElementById('modalContent');

        modalContent.innerHTML = this.generateRecordForm();
        modal.classList.remove('hidden');

        document.getElementById('recordForm').onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = {};

            for (const [key, value] of formData.entries()) {
                data[key] = value;
            }

            try {
                const response = await fetch(`/api/v1/databases/${this.databaseId}/records`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ data })
                });

                if (!response.ok) throw new Error('Failed to create record');

                await this.loadRecords();
                this.closeModal();

            } catch (error) {
                console.error('Error creating record:', error);
                alert('레코드 생성에 실패했습니다.');
            }
        };
    }

    generateRecordForm(record = null) {
        return `
            <form id="recordForm" class="space-y-4">
                ${Object.entries(this.schema).map(([id, property]) => `
                    <div>
                        <label class="block text-sm font-medium text-gray-700">
                            ${property.name}
                        </label>
                        ${this.generateInputField(property, record ? record.data[id] : null)}
                    </div>
                `).join('')}
                <div class="flex justify-end gap-2">
                    <button type="button"
                            onclick="closeModal()"
                            class="px-4 py-2 text-gray-700 bg-gray-100 rounded hover:bg-gray-200">
                        취소
                    </button>
                    <button type="submit"
                            class="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600">
                        저장
                    </button>
                </div>
            </form>
        `;
    }

    generateInputField(property, value = null) {
        switch (property.type) {
            case 'text':
                return `<input type="text"
                               name="${property.id}"
                               value="${value || ''}"
                               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">`;

            case 'number':
                return `<input type="number"
                               name="${property.id}"
                               value="${value || ''}"
                               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">`;

            case 'select':
                return `
                    <select name="${property.id}"
                            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                        <option value="">선택하세요</option>
                        ${property.options.map(option => `
                            <option value="${option}" ${value === option ? 'selected' : ''}>
                                ${option}
                            </option>
                        `).join('')}
                    </select>`;

            case 'multi_select':
                return `
                    <div class="mt-1 space-y-2">
                        ${property.options.map(option => `
                            <label class="inline-flex items-center">
                                <input type="checkbox"
                                       name="${property.id}"
                                       value="${option}"
                                       ${value?.includes(option) ? 'checked' : ''}
                                       class="rounded border-gray-300">
                                <span class="ml-2">${option}</span>
                            </label>
                        `).join('')}
                    </div>`;

            case 'date':
                return `<input type="date"
                               name="${property.id}"
                               value="${value || ''}"
                               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">`;

            case 'checkbox':
                return `
                    <label class="inline-flex items-center mt-1">
                        <input type="checkbox"
                               name="${property.id}"
                               ${value ? 'checked' : ''}
                               class="rounded border-gray-300">
                        <span class="ml-2">완료</span>
                    </label>`;

            default:
                return `<input type="text"
                               name="${property.id}"
                               value="${value || ''}"
                               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">`;
        }
    }

    async editRecord(recordId) {
        const record = this.records.find(r => r.id === recordId);
        if (!record) return;

        const modal = document.getElementById('modal');
        const modalContent = document.getElementById('modalContent');

        modalContent.innerHTML = this.generateRecordForm(record);
        modal.classList.remove('hidden');

        document.getElementById('recordForm').onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = {};

            for (const [key, value] of formData.entries()) {
                data[key] = value;
            }

            try {
                const response = await fetch(
                    `/api/v1/databases/${this.databaseId}/records/${recordId}`,
                    {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ data })
                    }
                );

                if (!response.ok) throw new Error('Failed to update record');

                await this.loadRecords();
                this.closeModal();

            } catch (error) {
                console.error('Error updating record:', error);
                alert('레코드 수정에 실패했습니다.');
            }
        };
    }

    async deleteRecord(recordId) {
        if (!confirm('정말 이 레코드를 삭제하시겠습니까?')) return;

        try {
            const response = await fetch(
                `/api/v1/databases/${this.databaseId}/records/${recordId}`,
                {
                    method: 'DELETE'
                }
            );

            if (!response.ok) throw new Error('Failed to delete record');

            await this.loadRecords();

        } catch (error) {
            console.error('Error deleting record:', error);
            alert('레코드 삭제에 실패했습니다.');
        }
    }

    // 뷰 렌더링 메서드
    switchView(viewType) {
        // 이전 뷰 숨기기
        document.querySelectorAll('[id$="View"]').forEach(view => {
            view.classList.add('hidden');
        });

        // 새로운 뷰 표시
        document.getElementById(`${viewType}View`).classList.remove('hidden');
        this.currentView = viewType;

        // 현재 뷰 텍스트 업데이트
        document.getElementById('currentView').textContent =
            viewType.charAt(0).toUpperCase() + viewType.slice(1);

        // 뷰에 맞게 레코드 다시 렌더링
        this.renderCurrentView();
    }

    renderCurrentView() {
        switch (this.currentView) {
            case 'table':
                this.renderTableView();
                break;
            case 'gallery':
                this.renderGalleryView();
                break;
            case 'board':
                this.renderBoardView();
                break;
            case 'calendar':
                this.renderCalendarView();
                break;
        }
    }

    renderTableView() {
        const tbody = document.getElementById('recordsList');
        tbody.innerHTML = this.records.map(record => `
            <tr>
                ${Object.entries(this.schema).map(([id, property]) => `
                    <td class="px-6 py-4 whitespace-nowrap">
                        ${this.formatValue(record.data[id], property)}
                    </td>
                `).join('')}
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm">
                    <button onclick="databaseManager.editRecord(${record.id})"
                            class="text-blue-600 hover:text-blue-900">
                        수정
                    </button>
                    <button onclick="databaseManager.deleteRecord(${record.id})"
                            class="ml-2 text-red-600 hover:text-red-900">
                        삭제
                    </button>
                </td>
            </tr>
        `).join('');
    }

    renderGalleryView() {
        const grid = document.getElementById('galleryGrid');
        grid.innerHTML = this.records.map(record => `
            <div class="bg-white rounded-lg shadow p-4">
                ${Object.entries(this.schema).map(([id, property]) => `
                    <div class="mb-2">
                        <div class="text-sm text-gray-500">${property.name}</div>
                        <div>${this.formatValue(record.data[id], property)}</div>
                    </div>
                `).join('')}
                <div class="mt-4 flex justify-end gap-2">
                    <button onclick="databaseManager.editRecord(${record.id})"
                            class="text-sm text-blue-600 hover:text-blue-900">
                        수정
                    </button>
                    <button onclick="databaseManager.deleteRecord(${record.id})"
                            class="text-sm text-red-600 hover:text-red-900">
                        삭제
                    </button>
                </div>
            </div>
        `).join('');
    }

    renderBoardView() {
        // 보드 뷰는 select 타입 속성을 기준으로 그룹화
        const boardColumns = document.getElementById('boardColumns');
        const selectProperty = Object.entries(this.schema)
            .find(([_, prop]) => prop.type === 'select');

        if (!selectProperty) {
            boardColumns.innerHTML = '<div>보드 뷰를 사용하려면 select 타입 속성이 필요합니다.</div>';
            return;
        }

        const [propertyId, property] = selectProperty;
        const groupedRecords = {};

        // 옵션별로 레코드 그룹화
        property.options.forEach(option => {
            groupedRecords[option] = this.records.filter(
                record => record.data[propertyId] === option
            );
        });

        boardColumns.innerHTML = Object.entries(groupedRecords)
            .map(([option, records]) => `
                <div class="flex-shrink-0 w-80">
                    <div class="bg-gray-100 rounded-lg p-4">
                        <h3 class="font-medium mb-4">${option}</h3>
                        <div class="space-y-3">
                            ${records.map(record => `
                                <div class="bg-white rounded shadow p-3">
                                    ${Object.entries(this.schema)
                                        .filter(([id]) => id !== propertyId)
                                        .map(([id, prop]) => `
                                            <div class="mb-1">
                                                <div class="text-xs text-gray-500">
                                                    ${prop.name}
                                                </div>
                                                <div class="text-sm">
                                                    ${this.formatValue(record.data[id], prop)}
                                                </div>
                                            </div>
                                        `).join('')}
                                    <div class="mt-2 flex justify-end gap-2">
                                        <button onclick="databaseManager.editRecord(${record.id})"
                                                class="text-xs text-blue-600 hover:text-blue-900">
                                            수정
                                        </button>
                                        <button onclick="databaseManager.deleteRecord(${record.id})"
                                                class="text-xs text-red-600 hover:text-red-900">
                                            삭제
                                        </button>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `).join('');
    }

    renderCalendarView() {
        const calendar = document.getElementById('calendar');
        const dateProperty = Object.entries(this.schema)
            .find(([_, prop]) => prop.type === 'date');

        if (!dateProperty) {
            calendar.innerHTML = '<div>캘린더 뷰를 사용하려면 date 타입 속성이 필요합니다.</div>';
            return;
        }

        const [propertyId] = dateProperty;
        const today = new Date();
        const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
        const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);

        // 달력 그리드 생성
        const days = [];
        const startPadding = firstDay.getDay();
        const totalDays = lastDay.getDate();

        for (let i = 0; i < startPadding; i++) {
            days.push(null);
        }

        for (let i = 1; i <= totalDays; i++) {
            days.push(new Date(today.getFullYear(), today.getMonth(), i));
        }

        calendar.innerHTML = `
            <div class="p-4">
                <div class="grid grid-cols-7 gap-2">
                    ${['일', '월', '화', '수', '목', '금', '토'].map(day => `
                        <div class="text-center font-medium">${day}</div>
                    `).join('')}
                    ${days.map(day => {
                        if (!day) return '<div class="h-32 bg-gray-50"></div>';

                        const dayRecords = this.records.filter(record => {
                            const recordDate = new Date(record.data[propertyId]);
                            return recordDate.toDateString() === day.toDateString();
                        });

                        return `
                            <div class="h-32 bg-white border p-2">
                                <div class="text-right text-gray-500">${day.getDate()}</div>
                                <div class="mt-1 space-y-1">
                                    ${dayRecords.map(record => `
                                        <div class="text-xs p-1 bg-blue-50 rounded">
                                            ${Object.entries(this.schema)
                                                .filter(([id]) => id !== propertyId)
                                                .slice(0, 1)
                                                .map(([id]) =>
                                                    record.data[id]
                                                ).join('')}
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    }

    formatValue(value, property) {
        if (value === null || value === undefined) return '-';

        switch (property.type) {
            case 'select':
            case 'text':
            case 'number':
                return value;

            case 'multi_select':
                return Array.isArray(value) ?
                    value.map(v => `<span class="inline-block px-2 py-1 text-xs bg-gray-100 rounded-full">${v}</span>`).join(' ') :
                    value;

            case 'date':
                return new Date(value).toLocaleDateString();

            case 'checkbox':
                return value ? '✓' : '✗';

            default:
                return value;
        }
    }

    closeModal() {
        document.getElementById('modal').classList.add('hidden');
    }
}

// 전역 인스턴스 생성
let databaseManager;

document.addEventListener('DOMContentLoaded', () => {
    const databaseId = window.location.pathname.split('/').pop();
    databaseManager = new DatabaseManager(databaseId);
});