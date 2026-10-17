---
name: requirement_elicitation
description: "Instructions for Lead BA on conducting high-leverage user interviews using ask_question, parsing raw user requests into SMART objectives, and formatting Gherkin user stories."
---

# Requirement Elicitation & PRD Formulation Skill

Kỹ năng này hướng dẫn `lead-ba` và `account-lead` thực hiện phỏng vấn làm rõ yêu cầu khách hàng:

## 1. Nguyên Tắc Phỏng Vấn (High-Leverage Interview)
- Chỉ đặt tối đa **1 đến 3 câu hỏi P0 then chốt**.
- Câu hỏi phải liên quan đến:
  1. Phạm vi MVP (Những gì BẮT BUỘC có trong phiên bản này).
  2. Phân quyền và người dùng mục tiêu (Ai dùng chức năng này, phân biệt User vs Admin).
  3. Quy tắc rẽ nhánh cốt lõi (Nếu gặp trường hợp ngoại lệ, hệ thống phản ứng ra sao).
- Gom câu hỏi thành trắc nghiệm, đánh dấu `(Recommended)` ở phương án tối ưu nhất.

## 2. Định Dạng User Story Chuẩn Gherkin
Mỗi User Story phải có cấu trúc:
```gherkin
Feature: <Tên tính năng>
  As a <Role/Persona>
  I want to <Action>
  So that <Business Value>

  Scenario: <Happy Path Scenario>
    Given <Tiền điều kiện>
    When <Hành động của người dùng>
    Then <Kết quả mong đợi>

  Scenario: <Edge Case 1 - Dữ liệu không hợp lệ>
    Given ...
    When ...
    Then ...

  Scenario: <Edge Case 2 - Xung đột hoặc mất kết nối>
    Given ...
    When ...
    Then ...
```
