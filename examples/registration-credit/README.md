# Registration-to-credit: first business workflow

用户选择的首个场景：**注册 → 填资 → KYC → 银行资料 → 授信**。

- [五阶段定义、转化公式与诊断边界](../../skills/growth-funnel-diagnosis/references/registration-credit.md)
- [匿名聚合采集模板](../../skills/growth-funnel-diagnosis/assets/registration-credit-intake.json)

实际业务的人数、时间窗口和生产事件定义尚待提供，因此业务转化率和瓶颈仍为未知。先验证五阶段同一cohort、去重、顺序和随访口径；再按未继续人数与转化率分别定位调查优先级；最后才设计实验。

授信暂按审批通过理解。银行资料暂按后端校验并保存理解，均须业务确认。

## 用合成数据跑通

在仓库根目录运行：

```sh
python3 skills/growth-funnel-diagnosis/scripts/analyze_registration_credit.py \
  examples/registration-credit/synthetic-intake.json --format markdown
```

[合成输入](synthetic-intake.json)中，1,000 人注册，224 人在固定窗口内授信通过，累计转化为 22.40%。注册到填资的未继续人数最多（300 人），KYC 到银行资料的相邻转化率最低（50.00%）。这两项排名回答不同的调查问题。

给 Agent 的任务：读取 Skill 和旅程口径，先跑合成样例复核分母及两个排名，再检查你提供的采集文件。确认授权、同一旅程和固定随访后才运行分析。若仍为空白或随访不足，返回缺失的字段和证据。
