# Project Contribution Template

Source template: `resources/2022-2023-HK2-GroupXX-Project Contribution.xlsx`

## Summary

| Field  | Value |
| ------ | ----- |
| Course |       |
| Class  |       |
| Group  |       |

## Project Metrics

| Metric                                    | Value | Note                                   |
| ----------------------------------------- | ----: | -------------------------------------- |
| Number of students working in the project |     5 | Input                                  |
| Number of tasks                           |    50 | Calculated from student task counts    |
| Number of task hours                      |   300 | Calculated from student task hours     |
| Number of Git commits                     |   100 | Calculated from student Git commits    |
| Max student percentage                    |   24% | Calculated from Percent column         |
| Project score                             | 8.225 | Entered by TA or estimated by students |

## Instructions

> Do not edit the grey cells. TAs will enter the score of all PAs in the project score and get the individual scores. Students can enter an estimated project score to see how percentages affects your scores.

> Use columns Tasks - Percent, Task Hours - Percent, Git - Percent as references for column Percent.

## Student Contribution Summary

| No | Student ID | Full name | Tasks | Tasks - Percent | Task Hours | Task Hours - Percent | Git Commits | Git - Percent | Percent | Score - Student | Score - TA |
| -- | ---------- | --------- | ----- | --------------- | ---------- | -------------------- | ----------- | ------------- | ------- | --------------- | ---------- |
| 1  |            |           | 10    | 20%             | 60         | 20%                  | 20          | 20%           | 23%     | 8.0             |            |
| 2  |            |           | 10    | 20%             | 60         | 20%                  | 20          | 20%           | 23%     | 8.0             |            |
| 3  |            |           | 10    | 20%             | 60         | 20%                  | 20          | 20%           | 23%     | 8.0             |            |
| 4  |            |           | 10    | 20%             | 60         | 20%                  | 20          | 25%           | 24%     | 8.225           |            |
| 5  |            |           | 10    | 20%             | 60         | 20%                  | 20          | 25%           | 7%      | 2.5             |            |

## Original Formula Reference

| Cell / Column        | Formula or rule                                                                         |
| -------------------- | --------------------------------------------------------------------------------------- |
| D7                   | `SUM(D17:D25)`                                                                        |
| D8                   | `SUM(F17:F25)`                                                                        |
| D9                   | `SUM(H17:H25)`                                                                        |
| D10                  | `MAX(J17:J25)`                                                                        |
| Tasks - Percent      | `IF($D$7=0, 0, Tasks / $D$7)`                                                         |
| Task Hours - Percent | `IF($D$8=0, 0, Task Hours / $D$8)`                                                    |
| Git - Percent        | `IF($D$9=0, 0, Git Commits / $D$9)`                                                   |
| Score - Student      | `IF(Percent=$D$10, $D$11, ROUND(2 * ($D$11 - $D$11 * (1 - Percent / $D$10)), 0) / 2)` |

## Tasks

A task should be done by only 1-2 students. Duplicate tasks are not recommended. Each member should work on at least 5 tasks.

| No  | Student ID | Full name       | Task Description                                                     | Hours | Evidence (screenshots of chat messages, of Git commits... proving that you perform and finish the task) |
| --- | ---------- | --------------- | -------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------- |
| 1   | 23127075   | Lê Trung Kiên | Tìm hiểu về DAST và viết doc                                    | 0.5   | ![1784735469770](image/Project_Contribution_Template/1784735469770.png)                                 |
| 2   | 23127075   | Lê Trung Kiên | Tìm hiểu về ZAP và viết doc                                     | 5     | ![1784735514655](image/Project_Contribution_Template/1784735514655.png)                                 |
| 3   | 23127075   | Lê Trung Kiên | Tìm hiểu về OWASP Top 10: 1; 2 và viết doc                      | 1     | ![1784735533992](image/Project_Contribution_Template/1784735533992.png)                                 |
| 4   | 23127075   | Lê Trung Kiên | Track Zap: Cài đặt và chạy Zap                                  | 5     |                                                                                                         |
| 5   | 23127075   | Lê Trung Kiên | Track Zap: Tạo flow Test với Zap, AI Triage (có báo cáo output) | 5     |                                                                                                         |
| 6   | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 7   | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 8   | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 9   | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 10  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 11  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 12  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 13  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 14  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 15  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 16  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 17  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 18  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 19  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 20  | 23127075   | Lê Trung Kiên |                                                                      |       |                                                                                                         |
| 21  |            |                 |                                                                      |       |                                                                                                         |
| 22  |            |                 |                                                                      |       |                                                                                                         |
| 23  |            |                 |                                                                      |       |                                                                                                         |
| 24  |            |                 |                                                                      |       |                                                                                                         |
| 25  |            |                 |                                                                      |       |                                                                                                         |
| 26  |            |                 |                                                                      |       |                                                                                                         |
| 27  |            |                 |                                                                      |       |                                                                                                         |
| 28  |            |                 |                                                                      |       |                                                                                                         |
| 29  |            |                 |                                                                      |       |                                                                                                         |
| 30  |            |                 |                                                                      |       |                                                                                                         |
| 31  |            |                 |                                                                      |       |                                                                                                         |
| 32  |            |                 |                                                                      |       |                                                                                                         |
| 33  |            |                 |                                                                      |       |                                                                                                         |
| 34  |            |                 |                                                                      |       |                                                                                                         |
| 35  |            |                 |                                                                      |       |                                                                                                         |
| 36  |            |                 |                                                                      |       |                                                                                                         |
| 37  |            |                 |                                                                      |       |                                                                                                         |
| 38  |            |                 |                                                                      |       |                                                                                                         |
| 39  |            |                 |                                                                      |       |                                                                                                         |
| 40  |            |                 |                                                                      |       |                                                                                                         |
| 41  |            |                 |                                                                      |       |                                                                                                         |
| 42  |            |                 |                                                                      |       |                                                                                                         |
| 43  |            |                 |                                                                      |       |                                                                                                         |
| 44  |            |                 |                                                                      |       |                                                                                                         |
| 45  |            |                 |                                                                      |       |                                                                                                         |
| 46  |            |                 |                                                                      |       |                                                                                                         |
| 47  |            |                 |                                                                      |       |                                                                                                         |
| 48  |            |                 |                                                                      |       |                                                                                                         |
| 49  |            |                 |                                                                      |       |                                                                                                         |
| 50  |            |                 |                                                                      |       |                                                                                                         |
| 51  |            |                 |                                                                      |       |                                                                                                         |
| 52  |            |                 |                                                                      |       |                                                                                                         |
| 53  |            |                 |                                                                      |       |                                                                                                         |
| 54  |            |                 |                                                                      |       |                                                                                                         |
| 55  |            |                 |                                                                      |       |                                                                                                         |
| 56  |            |                 |                                                                      |       |                                                                                                         |
| 57  |            |                 |                                                                      |       |                                                                                                         |
| 58  |            |                 |                                                                      |       |                                                                                                         |
| 59  |            |                 |                                                                      |       |                                                                                                         |
| 60  |            |                 |                                                                      |       |                                                                                                         |
| 61  |            |                 |                                                                      |       |                                                                                                         |
| 62  |            |                 |                                                                      |       |                                                                                                         |
| 63  |            |                 |                                                                      |       |                                                                                                         |
| 64  |            |                 |                                                                      |       |                                                                                                         |
| 65  |            |                 |                                                                      |       |                                                                                                         |
| 66  |            |                 |                                                                      |       |                                                                                                         |
| 67  |            |                 |                                                                      |       |                                                                                                         |
| 68  |            |                 |                                                                      |       |                                                                                                         |
| 69  |            |                 |                                                                      |       |                                                                                                         |
| 70  |            |                 |                                                                      |       |                                                                                                         |
| 71  |            |                 |                                                                      |       |                                                                                                         |
| 72  |            |                 |                                                                      |       |                                                                                                         |
| 73  |            |                 |                                                                      |       |                                                                                                         |
| 74  |            |                 |                                                                      |       |                                                                                                         |
| 75  |            |                 |                                                                      |       |                                                                                                         |
| 76  |            |                 |                                                                      |       |                                                                                                         |
| 77  |            |                 |                                                                      |       |                                                                                                         |
| 78  |            |                 |                                                                      |       |                                                                                                         |
| 79  |            |                 |                                                                      |       |                                                                                                         |
| 80  |            |                 |                                                                      |       |                                                                                                         |
| 81  |            |                 |                                                                      |       |                                                                                                         |
| 82  |            |                 |                                                                      |       |                                                                                                         |
| 83  |            |                 |                                                                      |       |                                                                                                         |
| 84  |            |                 |                                                                      |       |                                                                                                         |
| 85  |            |                 |                                                                      |       |                                                                                                         |
| 86  |            |                 |                                                                      |       |                                                                                                         |
| 87  |            |                 |                                                                      |       |                                                                                                         |
| 88  |            |                 |                                                                      |       |                                                                                                         |
| 89  |            |                 |                                                                      |       |                                                                                                         |
| 90  |            |                 |                                                                      |       |                                                                                                         |
| 91  |            |                 |                                                                      |       |                                                                                                         |
| 92  |            |                 |                                                                      |       |                                                                                                         |
| 93  |            |                 |                                                                      |       |                                                                                                         |
| 94  |            |                 |                                                                      |       |                                                                                                         |
| 95  |            |                 |                                                                      |       |                                                                                                         |
| 96  |            |                 |                                                                      |       |                                                                                                         |
| 97  |            |                 |                                                                      |       |                                                                                                         |
| 98  |            |                 |                                                                      |       |                                                                                                         |
| 99  |            |                 |                                                                      |       |                                                                                                         |
| 100 |            |                 |                                                                      |       |                                                                                                         |
