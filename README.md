# 商品采购管理系统数据库设计

## 1. 需求概述
根据题目要求，系统需要管理商品库存、供应商信息以及采购订单，并支持采购员、部门经理、系统管理员三种用户角色。

## 2. 数据字典
- `inventory`：商品库存档案
  - `item_id`：商品编码，主键
  - `name`：商品名称
  - `spec`：商品规格
  - `model`：商品型号
  - `size`：商品尺寸
  - `purchase_price`：进价
  - `sale_price`：销售价
  - `member_price`：会员价
  - `quantity`：在库数量
- `supplier`：供应商档案
  - `supplier_id`：供应商编码，主键
  - `name`：供应商名称
  - `contact`：联系人
  - `phone`：联系电话
  - `mobile`：手机
  - `address`：单位地址
  - `zipcode`：邮政编码
  - `bank`：开户银行
  - `account`：银行账号
- `supplier_item`：供应商供货表
  - `supplier_id`：供应商编码，外键
  - `item_id`：商品编码，外键
- `purchase_order`：订货单
  - `order_id`：订单编号，主键
  - `order_time`：订货时间
  - `supplier_id`：供应商编码，外键
  - `item_id`：商品编码，外键
  - `quantity`：订货数量
  - `price`：单价
  - `buyer`：采购员
  - `submit_time`：提交时间
  - `manager_comment`：部门经理审批意见
  - `approve_time`：审批时间
  - `approved`：是否通过
- `user`：系统用户
  - `user_id`：用户编号，主键
  - `username`：登录名
  - `password`：密码
  - `role`：角色（buyer/manager/admin）

## 3. E-R 模型
```
USER --< PURCHASE_ORDER >-- SUPPLIER
          |                  |
          v                  v
       INVENTORY          SUPPLIER_ITEM
```
简化表示：采购员创建采购订单，订单关联商品和供应商；部门经理对订单审批。供应商可供应多个商品。

## 4. 建表 SQL 示例
```sql
-- 商品库存表
CREATE TABLE inventory (
    item_id        VARCHAR(20) PRIMARY KEY,
    name           VARCHAR(100),
    spec           VARCHAR(50),
    model          VARCHAR(50),
    size           VARCHAR(50),
    purchase_price DECIMAL(10,2),
    sale_price     DECIMAL(10,2),
    member_price   DECIMAL(10,2),
    quantity       INT
);

-- 供应商表
CREATE TABLE supplier (
    supplier_id VARCHAR(20) PRIMARY KEY,
    name        VARCHAR(100),
    contact     VARCHAR(50),
    phone       VARCHAR(30),
    mobile      VARCHAR(30),
    address     VARCHAR(200),
    zipcode     VARCHAR(10),
    bank        VARCHAR(100),
    account     VARCHAR(50)
);

-- 供应商与商品关联表
CREATE TABLE supplier_item (
    supplier_id VARCHAR(20),
    item_id     VARCHAR(20),
    PRIMARY KEY (supplier_id, item_id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id),
    FOREIGN KEY (item_id) REFERENCES inventory(item_id)
);

-- 订货单表
CREATE TABLE purchase_order (
    order_id       VARCHAR(20) PRIMARY KEY,
    order_time     DATETIME,
    supplier_id    VARCHAR(20),
    item_id        VARCHAR(20),
    quantity       INT,
    price          DECIMAL(10,2),
    buyer          VARCHAR(20),
    submit_time    DATETIME,
    manager_comment VARCHAR(200),
    approve_time   DATETIME,
    approved       BOOLEAN,
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id),
    FOREIGN KEY (item_id) REFERENCES inventory(item_id),
    FOREIGN KEY (buyer) REFERENCES user(user_id)
);

-- 用户表
CREATE TABLE user (
    user_id  VARCHAR(20) PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100),
    role     ENUM('buyer','manager','admin')
);
```

## 5. 基本功能菜单（示例）
- **采购员**
  - 登录系统
  - 管理商品库存档案
  - 管理供应商档案
  - 填写和提交订货单
  - 查询订单审批结果
- **部门经理**
  - 登录系统
  - 审批采购员提交的订货单
  - 查询历史订单
- **系统管理员**
  - 管理所有用户
  - 管理商品、供应商、订单数据

## 6. 说明
以上 SQL 可在 MySQL 中直接执行创建数据库表。可根据需求编写基于 JDBC/ODBC 的应用程序，实现增删改查操作以及用户登录、菜单控制等功能。
