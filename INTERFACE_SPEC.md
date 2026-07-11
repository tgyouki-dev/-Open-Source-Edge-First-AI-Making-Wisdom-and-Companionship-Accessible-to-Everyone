# 📐 INTERFACE_SPEC.md - 生态协议详解

> **这是项目的"宪法"**  
> 所有参与者（无论贡献代码还是集成产品）都必须遵守这些接口标准。  
> 通过统一的接口，我们实现模块化、可组装、可扩展。

---

## 🎯 设计原则

```
接口是契约，实现是自由。

我们定义"说什么"（接口），
你们定义"怎么做"（实现）。

这样：
✅ 感知层可以独立演进（更换 YOLO v9、v10 等）
✅ 仲裁层可以独立演进（博弈论算法优化）
✅ 执行层可以独立演进（支持新硬件）
✅ 整个系统始终可协作
```

---

## 🔄 数据流三大关键接口

### 接口 A：感知层输出 (Layer 1 Output)

**职责**：感知层处理完毕，准备交给仲裁层的数据包

**核心字段**：

```json
{
  "timestamp": "ISO-8601",
  "impulses": [
    {
      "action_type": "EMERGENCY_ALERT | ROUTINE_TASK | LEARNING_OPPORTUNITY | ...",
      "urgency": 0.0-1.0,
      "confidence": 0.0-1.0,
      "modalities": {
        "vision": { "confidence": 0.92, "features": [...] },
        "audio": { "confidence": 0.85, "features": [...] },
        "tactile": { "confidence": 0.78, "features": [...] }
      },
      "reasoning": "Human-readable explanation"
    }
  ],
  "context": {
    "emotion_state": {
      "anxiety": 0.0-1.0,
      "fatigue": 0.0-1.0,
      "competitive": 0.0-1.0,
      "cautious": 0.0-1.0,
      "calm": 0.0-1.0,
      "trust": 0.0-1.0,
      "curiosity": 0.0-1.0,
      "engagement": 0.0-1.0
    },
    "system_resources": {
      "battery_percent": 0-100,
      "cpu_usage_percent": 0-100,
      "memory_available_mb": number,
      "temperature_celsius": number
    }
  }
}
```

**示例**：

```json
{
  "timestamp": "2024-07-11T20:30:45.123Z",
  "impulses": [
    {
      "action_type": "EMERGENCY_ALERT",
      "urgency": 0.95,
      "confidence": 0.92,
      "modalities": {
        "vision": { "confidence": 0.96 },
        "audio": { "confidence": 0.88 },
        "proprioceptive": { "confidence": 0.84 }
      },
      "reasoning": "Person on ground + distressed voice = fall detected"
    }
  ],
  "context": {
    "emotion_state": {
      "anxiety": 0.85,
      "fatigue": 0.2,
      "calm": 0.1,
      "trust": 0.7
    },
    "system_resources": {
      "battery_percent": 85,
      "cpu_usage_percent": 45
    }
  }
}
```

---

### 接口 B：仲裁层输出 (Layer 2 Output)

**职责**：仲裁层完成决策，准备交给执行层的指令包

**核心字段**：

```json
{
  "decision_id": "uuid",
  "timestamp": "ISO-8601",
  "primary_action": {
    "type": "CALL_EMERGENCY | ALERT_FAMILY | TURN_ON_LIGHTS | MOVE_TO_LOCATION | PLAY_AUDIO | ...",
    "parameters": { "...": "action-specific params" },
    "priority": 0-10,
    "safety_level": "SAFE | CAUTION | CRITICAL"
  },
  "fallback_actions": [
    { "type": "...", "parameters": {} }
  ],
  "execution_deadline_ms": 50,
  "reasoning_trace": [
    { "step": "Logic Consistency Check", "status": "PASS", "details": "..." },
    { "step": "Safety Assessment", "status": "PASS", "details": "..." }
  ],
  "conflict_analysis": {
    "detected_conflicts": [
      {
        "impulse_a": "...",
        "impulse_b": "...",
        "conflict_type": "SAFETY_VS_PRIVACY | SPEED_VS_ACCURACY | ...",
        "nash_equilibrium_value": 0.87
      }
    ]
  }
}
```

**示例**：

```json
{
  "decision_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-07-11T20:30:45.145Z",
  "primary_action": {
    "type": "CALL_EMERGENCY",
    "priority": 10,
    "safety_level": "CRITICAL",
    "parameters": {
      "emergency_service": "911",
      "location": { "latitude": 40.7128, "longitude": -74.0060 }
    }
  },
  "fallback_actions": [
    { "type": "ALERT_FAMILY", "parameters": { "contacts": ["family@example.com"] } }
  ],
  "execution_deadline_ms": 45,
  "reasoning_trace": [
    { "step": "Logic Consistency Check", "status": "PASS" },
    { "step": "Safety Assessment", "status": "PASS" }
  ]
}
```

---

### 接口 C：执行层反馈 (Layer 3 Feedback)

**职责**：执行层完成行动后，返回执行结果

**核心字段**：

```json
{
  "decision_id": "uuid",
  "timestamp": "ISO-8601",
  "execution_status": "SUCCESS | PARTIAL | FAILED | TIMEOUT",
  "action_results": [
    {
      "action_type": "string",
      "status": "SUCCESS | FAILED | SKIPPED",
      "actual_execution_time_ms": number,
      "error_message": "optional"
    }
  ],
  "outcome_assessment": {
    "intended_outcome_achieved": true,
    "confidence": 0.95,
    "learning_signal": { "...": "signal for memory system" }
  }
}
```

---

## 🔌 模块级接口规范

### 感知层 (Perception Layer)

```python
class PerceptionLayerInterface:
    def process_frame(self, 
                     camera_frame: np.ndarray,      # Shape (H, W, 3)
                     audio_chunk: np.ndarray,        # Shape (samples,)
                     sensor_readings: Dict,
                     timestamp: datetime
                     ) -> PerceptionOutput:
        pass
```

**性能要求**：
| 指标 | 要求 |
|------|------|
| 处理延迟 | <5ms |
| 内存占用 | <100MB |
| CPU 占用 | <25% (单核) |
| 特征维度 | 128D-512D |

---

### 博弈仲裁层 (Arbitration Layer)

```python
class ArbitrationLayerInterface:
    def arbitrate(self, 
                 perception_output: PerceptionOutput,
                 historical_decisions: List[ArbitrationDecision],
                 user_preferences: Dict
                 ) -> ArbitrationDecision:
        """必须实现：
        1. 逻辑一致性检查
        2. 安全性评估
        3. 物理可行性检查
        4. 约束求解
        5. 纳什均衡计算
        """
        pass
```

**性能要求**：
| 指标 | 要求 |
|------|------|
| 决策延迟 | <15ms |
| 可解释性 | 每个决策必须包含 reasoning_trace |
| 冲突处理 | 支持 3+ 个相互冲突的冲动 |

---

### 执行层 (Execution Layer)

```python
class ExecutionLayerInterface:
    def execute(self, 
               decision: ArbitrationDecision,
               actuator_config: Dict
               ) -> ExecutionFeedback:
        """支持的执行模式：
        1. 串行执行 - 按优先级顺序
        2. 并行执行 - 不相关操作并行
        3. 时间受限 - 必须在 deadline_ms 内
        """
        pass
```

**性能要求**：
| 指标 | 要求 |
|------|------|
| 执行延迟 | <15ms |
| 失败恢复 | <10ms |
| 硬件抽象 | 支持多种执行器 |

---

## 📦 数据格式统一规范

所有 JSON 数据必须：

1. **UTF-8 编码**
2. **包含 timestamp（ISO 8601 格式）**
3. **包含 metadata（版本、来源）**
4. **支持向后兼容**
5. **大小限制**：
   - PerceptionOutput: <2MB
   - ArbitrationDecision: <100KB
   - ExecutionFeedback: <500KB

---

## 🔗 集成检查清单

实现新模块时，确保：

- [ ] 输入输出符合相应的 JSON Schema
- [ ] 性能指标达到表中要求
- [ ] 包含完整的 error handling
- [ ] 包含日志和 tracing
- [ ] 编写单元测试（>80% coverage）
- [ ] 提供使用示例
- [ ] 文档齐全（README + API docs）

