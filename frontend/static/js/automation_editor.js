
class AutomationEditor {
    constructor(container) {
        this.container = container;
        this.rule = null;
        this.initializeUI();
    }

    initializeUI() {
        this.container.innerHTML = `
            <div class="p-4 space-y-6">
                <!-- 기본 정보 -->
                <div>
                    <label class="block text-sm font-medium text-gray-700">규칙 이름</label>
                    <input type="text" id="ruleName" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                </div>

                <!-- 트리거 설정 -->
                <div>
                    <label class="block text-sm font-medium text-gray-700">트리거</label>
                    <select id="triggerType" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                        <option value="on_create">레코드 생성 시</option>
                        <option value="on_update">레코드 업데이트 시</option>
                        <option value="on_delete">레코드 삭제 시</option>
                        <option value="scheduled">예약 실행</option>
                        <option value="condition_met">조건 충족 시</option>
                    </select>

                    <div id="scheduleConfig" class="mt-2 hidden">
                        <label class="block text-sm font-medium text-gray-700">실행 주기</label>
                        <input type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                               placeholder="예: 1h (1시간마다), 1d (1일마다)">
                    </div>
                </div>

                <!-- 조건 설정 -->
                <div>
                    <label class="block text-sm font-medium text-gray-700">조건</label>
                    <div id="conditionBuilder" class="mt-2 space-y-2">
                        <!-- 조건 빌더 UI가 여기에 동적으로 추가됨 -->
                    </div>
                    <button type="button" onclick="addCondition()"
                            class="mt-2 text-sm text-blue-600 hover:text-blue-500">
                        + 조건 추가
                    </button>
                </div>

                <!-- 액션 설정 -->
                <div>
                    <label class="block text-sm font-medium text-gray-700">액션</label>
                    <div id="actionBuilder" class="mt-2 space-y-4">
                        <!-- 액션 설정 UI가 여기에 동적으로 추가됨 -->
                    </div>
                    <button type="button" onclick="addAction()"
                            class="mt-2 text-sm text-blue-600 hover:text-blue-500">
                        + 액션 추가
                    </button>
                </div>

                <!-- 저장 버튼 -->
                <div class="flex justify-end">
                    <button type="button" onclick="saveRule()"
                            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                        규칙 저장
                    </button>
                </div>
            </div>
        `;

        this.setupEventListeners();
    }

    setupEventListeners() {
        // 트리거 타입 변경 시 관련 설정 UI 표시/숨김
        document.getElementById('triggerType').addEventListener('change', (e) => {
            const scheduleConfig = document.getElementById('scheduleConfig');
            scheduleConfig.style.display = e.target.value === 'scheduled' ? 'block' : 'none';
        });
    }

    addCondition() {
        const conditionBuilder = document.getElementById('conditionBuilder');
        const conditionDiv = document.createElement('div');
        conditionDiv.className = 'flex gap-2 items-center';
        conditionDiv.innerHTML = `
            <select class="flex-1 rounded-md border-gray-300 shadow-sm">
                <option value="">필드 선택</option>
                <!-- 데이터베이스의 필드들이 동적으로 추가됨 -->
            </select>
            <select class="flex-1 rounded-md border-gray-300 shadow-sm">
                <option value="equals">같음</option>
                <option value="not_equals">같지 않음</option>
                <option value="contains">포함</option>
                <option value="greater_than">보다 큼</option>
                <option value="less_than">보다 작음</option>
            </select>
            <input type="text" class="flex-1 rounded-md border-gray-300 shadow-sm"
                   placeholder="값">
            <button type="button" onclick="this.parentElement.remove()"
                    class="text-red-600 hover:text-red-500">
                삭제
            </button>
        `;
        conditionBuilder.appendChild(conditionDiv);
    }

    addAction() {
        const actionBuilder = document.getElementById('actionBuilder');
        const actionDiv = document.createElement('div');
        actionDiv.className = 'border rounded p-4';
        actionDiv.innerHTML = `
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">액션 타입</label>
                    <select class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                            onchange="showActionConfig(this)">
                        <option value="update_record">레코드 업데이트</option>
                        <option value="create_record">레코드 생성</option>
                        <option value="send_notification">알림 전송</option>
                        <option value="api_call">API 호출</option>
                    </select>
                </div>

                <div class="action-config">
                    <!-- 액션 타입별 설정 UI가 여기에 동적으로 추가됨 -->
                </div>

                <button type="button" onclick="this.closest('.border').remove()"
                        class="text-red-600 hover:text-red-500">
                    액션 삭제
                </button>
            </div>
        `;
        actionBuilder.appendChild(actionDiv);
    }

    showActionConfig(select) {
        const configContainer = select.closest('div').nextElementSibling;
        const actionType = select.value;

        let configHTML = '';
        switch (actionType) {
            case 'update_record':
                configHTML = `
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">업데이트할 필드</label>
                            <div id="updateFields" class="space-y-2">
                                <div class="flex gap-2">
                                    <select class="flex-1 rounded-md border-gray-300 shadow-sm">
                                        <option value="">필드 선택</option>
                                        <!-- 데이터베이스의 필드들이 동적으로 추가됨 -->
                                    </select>
                                    <input type="text" class="flex-1 rounded-md border-gray-300 shadow-sm"
                                           placeholder="값">
                                </div>
                            </div>
                            <button type="button" onclick="addUpdateField(this)"
                                    class="mt-2 text-sm text-blue-600 hover:text-blue-500">
                                + 필드 추가
                            </button>
                        </div>
                    </div>
                `;
                break;

            case 'send_notification':
                configHTML = `
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">알림 채널</label>
                            <select class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                                <option value="email">이메일</option>
                                <option value="webhook">웹훅</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700">수신자</label>
                            <input type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                   placeholder="이메일 주소 또는 웹훅 URL">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700">제목</label>
                            <input type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                   placeholder="알림 제목">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700">메시지</label>
                            <textarea class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                      placeholder="알림 내용"></textarea>
                            <p class="mt-1 text-sm text-gray-500">
                                필드 값을 사용하려면 {{필드명}} 형식으로 입력하세요.
                            </p>
                        </div>
                    </div>
                `;
                break;

            case 'api_call':
                configHTML = `
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">요청 방법</label>
                            <select class="mt-1 block w-full rounded-md border-gray-300 shadow-sm">
                                <option value="GET">GET</option>
                                <option value="POST">POST</option>
                                <option value="PUT">PUT</option>
                                <option value="DELETE">DELETE</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700">URL</label>
                            <input type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                   placeholder="https://api.example.com/endpoint">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700">요청 헤더</label>
                            <div id="headers" class="space-y-2">
                                <div class="flex gap-2">
                                    <input type="text" class="flex-1 rounded-md border-gray-300 shadow-sm"
                                           placeholder="헤더명">
                                    <input type="text" class="flex-1 rounded-md border-gray-300 shadow-sm"
                                           placeholder="값">
                                </div>
                            </div>
                            <button type="button" onclick="addHeader(this)"
                                    class="mt-2 text-sm text-blue-600 hover:text-blue-500">
                                + 헤더 추가
                            </button>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700">요청 본문</label>
                            <textarea class="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                                      placeholder="JSON 형식의 요청 본문"></textarea>
                        </div>
                    </div>
                `;
                break;
        }

        configContainer.innerHTML = configHTML;
    }

    getFormData() {
        const rule = {
            name: document.getElementById('ruleName').value,
            trigger: {
                type: document.getElementById('triggerType').value,
            },
            conditions: this.getConditions(),
            actions: this.getActions(),
            enabled: true
        };

        // 스케줄 설정이 있는 경우 추가
        if (rule.trigger.type === 'scheduled') {
            const scheduleInput = document.querySelector('#scheduleConfig input');
            rule.trigger.schedule = {
                interval: scheduleInput.value
            };
        }

        return rule;
    }

    getConditions() {
        const conditions = [];
        document.querySelectorAll('#conditionBuilder > div').forEach(div => {
            const selects = div.querySelectorAll('select');
            const input = div.querySelector('input');

            conditions.push({
                property: selects[0].value,
                operator: selects[1].value,
                value: input.value
            });
        });

        return {
            type: 'and',
            conditions: conditions
        };
    }

    getActions() {
        const actions = [];
        document.querySelectorAll('#actionBuilder > div').forEach(div => {
            const actionType = div.querySelector('select').value;
            const config = this.getActionConfig(div, actionType);
            actions.push({
                type: actionType,
                ...config
            });
        });

        return actions;
    }

    getActionConfig(div, actionType) {
        const config = {};

        switch (actionType) {
            case 'update_record':
                config.data = {};
                div.querySelectorAll('#updateFields > div').forEach(field => {
                    const selects = field.querySelectorAll('select');
                    const input = field.querySelector('input');
                    config.data[selects[0].value] = input.value;
                });
                break;

            case 'send_notification':
                const notificationInputs = div.querySelectorAll('input, select, textarea');
                config.template = {
                    channel: notificationInputs[0].value,
                    to: notificationInputs[1].value,
                    subject: notificationInputs[2].value,
                    message: notificationInputs[3].value
                };
                break;

            case 'api_call':
                config.method = div.querySelector('select').value;
                config.url = div.querySelector('input[placeholder*="URL"]').value;
                config.headers = {};
                div.querySelectorAll('#headers > div').forEach(header => {
                    const inputs = header.querySelectorAll('input');
                    config.headers[inputs[0].value] = inputs[1].value;
                });
                config.data = JSON.parse(div.querySelector('textarea').value || '{}');
                break;
        }

        return config;
    }

    async saveRule() {
        const rule = this.getFormData();

        try {
            const response = await fetch('/api/v1/automation/rules', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(rule)
            });

            if (!response.ok) {
                throw new Error('Failed to save automation rule');
            }

            alert('자동화 규칙이 저장되었습니다.');
            window.location.reload();
        } catch (error) {
            console.error('Error saving rule:', error);
            alert('자동화 규칙 저장에 실패했습니다.');
        }
    }
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('#automationEditor');
    if (container) {
        new AutomationEditor(container);
    }
});