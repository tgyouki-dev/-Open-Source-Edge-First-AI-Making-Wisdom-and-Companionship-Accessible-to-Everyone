# 🤝 CONTRIBUTING.md - 贡献指南

> 欢迎来革命！但有一个前提：**遵循博弈论原则，而不是简单加参数。**

---

## 🎯 我们的核心信念

```
❌ 错误的方式: "再加一个参数来支持新功能"
   代码会变成：config = {..., param_47, param_48, param_49, ...}

✅ 正确的方式: "如何用博弈论来优雅地处理这个冲突？"
   代码会变成：arbitrator.resolve(impulse_a, impulse_b, context)
```

**这就是我们与传统AI框架的区别。**

---

## 📋 贡献前的心理建设

在提交 PR 之前，问自己：

### 1️⃣ 这是"新功能"还是"博弈问题"？

```python
❌ 错误示范：
"我想加一个新参数 enable_quiet_mode"

✅ 正确示范：
"我发现了一个冲突：用户想安静，但系统需要警报。
我提议通过情绪系统的权重调整来解决这个博弈问题。
当 quiet_preference > 0.8 时，警报优先级降低，但安全警报仍保持最高。"
```

### 2️⃣ 这会违反"三层架构"吗？

```
Layer 1: 感知 ✓
  新增视觉模块？OK，这是感知增强

Layer 2: 博弈仲裁 ✓✓✓
  新增约束条件？YES！这是我们最欢迎的贡献

Layer 3: 执行 ✓
  新增执行器支持？OK，这是执行能力扩展

❌ 跨越层的"魔法参数"？NO！
```

### 3️⃣ 这能通过"45ms 延迟测试"吗？

```
完整决策循环必须 <50ms：
- 感知: <5ms
- 博弈仲裁: <20ms
- 执行: <15ms
- 反馈: <5ms

如果你的功能破坏了这个指标，
它就不能合并，除非：
1. 可选且默认关闭
2. 提供了等效的低延迟实现
```

---

## 🚀 如何正确贡献

### Step 1: 找一个"博弈问题"

首先浏览 [Issues](https://github.com/tgyouki-dev/edge-first-ai/issues)，寻找标记为以下的问题：

```
🎮 game-theory: 需要新的约束条件或仲裁规则
🧠 emotion-system: 情绪维度的扩展
⚡ performance: 延迟优化
🔐 safety: 安全性改进
```

**优先贡献顺序**：

1. 🎮 博弈论改进 (最高优先级)
2. 🧠 情绪系统扩展
3. ⚡ 性能优化
4. 🔐 安全特性
5. 📚 文档改进

### Step 2: 提出 Issue（设计阶段）

**不要直接写代码！** 先在 Issue 中讨论设计。

```markdown
## 标题
[PROPOSAL] 多目标冲突的帕累托优化

## 问题描述
当系统面临 3 个以上的互斥冲动时，
当前的两两对比方法不够优雅。

## 提议方案
引入 Pareto Frontier 概念：
1. 生成所有可能的决策组合
2. 筛选出"非劣"方案（无法同时改进所有目标）
3. 根据上下文权重选择最优点

## 博弈论依据
这遵循"帕累托最优"原则：
- 无法通过改变方案让某一方更好
- 而不让其他方变差

## 性能影响
预计 Layer 2 延迟从 15ms → 18ms（接受范围内）

## 伪代码
```python
frontier = compute_pareto_frontier(impulses)
optimal = frontier.select_by_weights(context_weights)
```
```

### Step 3: 获得反馈

维护者会评论你的 Issue：

```
✅ 同意设计
📝 要求修改细节
❌ 不符合项目方向
```

**只有获得 ✅ 后，才开始写代码。**

### Step 4: Fork & 创建分支

```bash
# Fork 项目
git clone https://github.com/YOUR_USERNAME/edge-first-ai.git
cd edge-first-ai

# 创建分支（命名规范很重要！）
git checkout -b game-theory/pareto-optimization
#           ↑ 类别    ↑ 简洁描述

# 可用的分支前缀：
# game-theory/...     - 博弈论改进
# emotion/...         - 情绪系统
# perf/...            - 性能优化
# safety/...          - 安全特性
# bugfix/...          - 问题修复
# docs/...            - 文档
```

### Step 5: 代码标准

#### 🎮 博弈论代码风格

```python
# ✅ 正确示范：清晰的博弈论意图

class ParetoOptimizationArbitrator(BaseArbitrator):
    """
    使用帕累托优化处理多目标冲突。
    
    博弈论原理：
    - 生成 Pareto frontier 上的所有非劣方案
    - 避免选择"被完全支配"的方案
    - 根据上下文权重在 frontier 上选择最优点
    """
    
    def arbitrate(self, impulses: List[Impulse], 
                  context: Context) -> Decision:
        """在 <20ms 内完成仲裁"""
        
        # Step 1: 初步筛选（安全性约束）
        safe_impulses = [i for i in impulses if i.safety_level >= 0.5]
        
        # Step 2: 计算 Pareto frontier
        frontier = self._compute_pareto_frontier(safe_impulses)
        
        # Step 3: 根据情绪和上下文权重选择最优点
        weights = self._compute_weights(context)
        optimal = frontier.max_weighted_score(weights)
        
        return Decision(
            action=optimal.action,
            reasoning={
                'method': 'pareto_optimization',
                'frontier_size': len(frontier),
                'confidence': optimal.score
            }
        )
```

#### ❌ 错误示范：参数堆砌

```python
# ❌ 不要这样做！

def arbitrate(self, impulses, 
              weight_safety=0.8,
              weight_urgency=0.6,
              weight_resources=0.4,
              weight_emotion=0.5,
              weight_user_preference=0.7,
              weight_historical_success=0.5,
              param_1=0.3,  # ← 这是什么？
              param_2=0.2,  # ← 这又是什么？
              ...):
    # 50 行嵌套 if 语句
    pass
```

### Step 6: 测试

```bash
# 运行单元测试
pytest tests/ -v

# 性能测试（确保 <50ms）
python tests/performance_test.py

# 功能测试（确保博弈论逻辑正确）
python tests/game_theory_test.py

# 集成测试（确保不破坏现有功能）
python tests/integration_test.py
```

### Step 7: 文档

每个新的博弈论方法都需要文档：

```markdown
## 新方法：帕累托优化仲裁

### 问题
之前的两两对比方法在 3+ 冲动时不够优雅。

### 解决方案
使用帕累托前沿来选择"非劣"方案。

### 博弈论基础
- 帕累托最优：无法同时改进所有目标
- 纳什均衡：每个参与者都选择最优应对
- 权重调整：根据上下文动态权衡

### 使用示例
```python
arbitrator = ParetoOptimizationArbitrator()
decision = arbitrator.arbitrate(impulses, context)
```

### 性能数据
- 时间复杂度：O(n²)，其中 n = 冲动数量
- 延迟影响：+3ms（可接受）
- 通过所有测试：✅
```

### Step 8: 提交 PR

```markdown
## PR 标题
[ENHANCEMENT] 帕累托优化仲裁算法

## 关联 Issue
Closes #42

## 变更描述
实现了基于帕累托前沿的多目标冲突解决方案。

## 博弈论验证清单
- [x] 遵循纳什均衡原则
- [x] 优先级加权合理
- [x] 完全通过单元测试
- [x] 延迟 <50ms

## 性能影响
- Layer 2 延迟：15ms → 18ms (+20%)
- 整体延迟：45ms → 48ms (可接受)
- 通过压力测试：20+ 并发冲动 ✅

## 测试覆盖率
- 新增代码覆盖率：95%+
- 集成测试通过：✅
- 回归测试通过：✅

## 截图/演示
[如果适用]
```

---

## ✅ PR 审查清单

维护者会检查以下内容：

### 设计检查
- [ ] 遵循博弈论原则
- [ ] 符合三层架构
- [ ] 没有"魔法参数"

### 代码检查
- [ ] 代码可读性高
- [ ] 有清晰的注释
- [ ] 遵循项目风格指南

### 性能检查
- [ ] 延迟 <50ms
- [ ] 内存占用合理
- [ ] 通过压力测试

### 测试检查
- [ ] 覆盖率 >90%
- [ ] 单元测试通过
- [ ] 集成测试通过

### 文档检查
- [ ] 有清晰的文档
- [ ] 博弈论原理已解释
- [ ] 使用示例完整

---

## 🏆 优秀贡献者标志

你可能会获得以下标签：

```
🎮 Game Theory Expert
   - 贡献了 3+ 博弈论相关的 PR
   
🧠 Emotion Specialist  
   - 扩展了情绪系统维度
   
⚡ Performance Optimizer
   - 优化了延迟，达到 <50ms 目标
   
🔐 Safety Guardian
   - 增强了系统安全性
   
📚 Documentation Hero
   - 贡献了 1000+ 字的高质量文档
```

---

## 💬 常见问题

### Q: 我想加一个新的参数来控制行为，行吗？

**A**: 不行！提一个 Issue，我们一起设计一个博弈论方案来解决这个问题。

```
❌ 你的提议: enable_turbo_mode=True
✅ 我们的方案: 添加新的约束条件到仲裁法庭
```

### Q: 我的代码延迟是 55ms，超过了 50ms，怎么办？

**A**: 两个选项：

1. 优化你的代码，达到 <50ms
2. 如果这是可选特性，标记为 `optional: True` 和 `default: False`

```python
@optional_feature(default=False)
def my_feature():
    """延迟 55ms，需要用户显式启用"""
    pass
```

### Q: 我想改变现有的博弈论规则，行吗？

**A**: 可以，但需要：

1. 在 Issue 中详细解释为什么现有规则不好
2. 提出新的博弈论基础
3. 展示性能对比
4. 维护者同意后才能改

```markdown
## 提议改变 Layer 2 的权重计算

### 现状
权重是静态的，不考虑历史成功率。

### 问题
这导致系统无法从失败中学习。

### 提议
加入"历史成功率"作为动态权重因子。

### 数据支持
通过过去 1000 次决策的分析，
新权重会提高 23% 的正确决策率。

### 性能影响
查询历史记忆需要 +2ms。
总延迟仍在 <50ms。
```

### Q: 我可以用其他许可证发布基于你代码的产品吗？

**A**: 可以！MIT 许可证允许这样做。只需保留许可证声明。

---

## 🎓 学习资源

如果你对博弈论不熟悉，建议阅读：

### 📖 推荐书籍
- 《博弈论基础》- Thomas Ferguson
- 《竞争与合作》- John Nash

### 📺 视频教程
- MIT OpenCourseWare: Game Theory
- Khan Academy: Game Theory Basics

### 🔗 相关论文
- Nash Equilibrium in Multi-Agent Systems
- Pareto Optimization in Real-Time Decision Making

---

## 🚀 贡献的最佳实践

### 1️⃣ 小而精的 PR
不要一次改变整个系统。一次一个功能。

### 2️⃣ 充分的讨论
在代码前充分讨论。70% 的时间用在设计，30% 用在代码。

### 3️⃣ 清晰的博弈论原理
每个改进都应该能用博弈论术语解释。

### 4️⃣ 充分的测试
新代码必须有 >90% 的测试覆盖率。

### 5️⃣ 文档优先
文档和代码同步提交。

---

## 🎉 你的贡献将如何被使用

你的代码可能会被用在：

- 🚗 **特斯拉自动驾驶** - 我们的博弈论仲裁适合实时驾驶
- 🏠 **家庭陪伴机器人** - 你的情绪系统扩展让AI更温暖
- 🏭 **工业机器控制** - 你的安全约束让工厂更安全
- 🌍 **全球开源生态** - 你的代码帮助世界各地的开发者

**你不只是在写代码，你在改变世界。**

---

## 📞 需要帮助？

- 💬 **Discussions** - https://github.com/tgyouki-dev/edge-first-ai/discussions
- 🐛 **Issues** - https://github.com/tgyouki-dev/edge-first-ai/issues
- 📧 **Email** - tgyouki@gmail.com

---

**欢迎加入革命！让我们一起构建更聪明、更有温度、更民主的 AI 系统。** 🚀❤️
