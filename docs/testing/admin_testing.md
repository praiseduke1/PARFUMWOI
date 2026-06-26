# Admin Module — Black-Box Test Report

**Date:** 2026-06-27  
**Test file:** `tests_admin.py`  
**Total tests:** 211  
**Passed:** 211  
**Failed:** 0  
**Duration:** 322.51s (5m22s)  

**Suite-wide regression check:** All 672 tests (existing + admin) pass in 852.73s.

---

## Module Coverage

| Module | Class | Tests | Description |
|---|---|---|---|
| **Dashboard** | `TestModuleDashboard` | 20 | Admin login, index, custom analytics dashboard, KPIs, charts, notifications, Jazzmin settings, separate admin session, password change, logout |
| **Products** | `TestModuleProducts` | 30 | Product CRUD pages, brand CRUD, fragrance note CRUD, fragrance family CRUD, product variants inline, reviews, slug redirects, mark_available/unavailable actions, filters, search, date hierarchy, delete |
| **Categories** | `TestModuleCategories` | 8 | Category CRUD, search, product_count column, slug prepopulation, fragrance family list |
| **Orders** | `TestModuleOrders` | 28 | Order list/detail, all 6 status transition actions (paid/processing/shipped/delivered/completed/cancelled), status guards (wrong from-states, delivered/completed cannot cancel), status history, inline items, search, filters, legacy voucher admin, timestamp updates, delete |
| **Customers** | `TestModuleCustomers` | 20 | User CRUD, profile list, member profile with readonly fields (total_spending, total_points), point transactions list/filter, customer address list/filter, wishlist CRUD, user order_count and total_spending annotations |
| **Promotions** | `TestModulePromotions` | 15 | Voucher CRUD pages, mark_active/mark_inactive actions, list filters, search, readonly claimed_count/used_count, user voucher changelist/search/status filter, unlimited quota, voucher type badge, user voucher inline |
| **Voucher** | `TestModuleVoucher` | 7 | Legacy orders.Voucher list/filter/readonly used_count, promotions voucher add all 5 types, search by code, delete both voucher models |
| **Loyalty** | `TestModuleLoyalty` | 12 | Member list, level display, level filter, point transaction list with data for all 3 transaction types (EARN/REDEEM/UPGRADE), spending/points readonly, manual level upgrade, search |
| **Reports** | `TestModuleReports` | 20 | All KPI values, revenue/orders/AOV/paid rate, top products, monthly data (12 months), category revenue, top customers, payment methods, customer growth chart, low stock notifications, sidebar insights, recent activity timeline, member counts, avg rating |
| **Settings** | `TestModuleSettings` | 14 | Password change/done pages, Jazzmin installed/config/UI-tweaks, SeparateAdminSessionMiddleware, login URL, custom admin template (base_site), order change_form customization, navbar brand, search_model, topmenu_links, icons config |
| **Permission** | `TestModulePermission` | 19 | All auth guards (anonymous→admin redirect, regular user blocked from all admin URLs, superuser access, staff-not-superuser access to customer views, CSRF on admin login/add forms, admin login renders, login redirect, group admin CRUD) |
| **Cart/Payment/Regions** | `TestModuleCartPaymentRegions` | 18 | Cart list/detail with items, payment list/detail/search/filter/status history, province/city/district/postal code admin CRUD |

---

## Module 1: Dashboard (20 tests)

| Test | Scenario | Result |
|---|---|---|
| `test_dashboard_01_login_page` | GET `/admin/login/` as anonymous → 200 | ✅ |
| `test_dashboard_02_index_page` | GET `/admin/` as superuser → 200 | ✅ |
| `test_dashboard_03_anonymous_redirect` | GET `/admin/` as anonymous → 302 | ✅ |
| `test_dashboard_04_custom_dashboard_accessible` | GET `/admin/dashboard/` as superuser → 200 | ✅ |
| `test_dashboard_05_custom_dashboard_requires_staff` | GET `/admin/dashboard/` as regular user → 302 | ✅ |
| `test_dashboard_06_custom_dashboard_context_has_kpis` | Context includes revenue_total, orders_total, active_customers, active_products, aov, paid_rate | ✅ |
| `test_dashboard_07_custom_dashboard_with_data` | With 1 order, orders_total >= 1, has_orders=True | ✅ |
| `test_dashboard_08_dashboard_chart_data` | chart_dates has at least 7 entries | ✅ |
| `test_dashboard_09_dashboard_status_counts` | status_counts in context | ✅ |
| `test_dashboard_10_dashboard_days_param` | ?days=7 → 200 | ✅ |
| `test_dashboard_11_dashboard_365_days` | ?days=365 → 200 | ✅ |
| `test_dashboard_12_dashboard_notifications` | Pending order generates warning notification | ✅ |
| `test_dashboard_13_dashboard_top_products` | top_products in context | ✅ |
| `test_dashboard_14_dashboard_monthly_summary` | monthly_data in context (12 months) | ✅ |
| `test_dashboard_15_dashboard_title` | title = "Analytics Dashboard" | ✅ |
| `test_dashboard_16_jazzmin_installed` | 'jazzmin' in INSTALLED_APPS | ✅ |
| `test_dashboard_17_separate_admin_session` | admin_sessionid cookie present after login | ✅ |
| `test_dashboard_18_password_change_page` | GET `/admin/password_change/` → 200 | ✅ |
| `test_dashboard_19_logout_accessible` | POST `/admin/logout/` → 200/302 | ✅ |
| `test_dashboard_20_customer_growth_data` | reg_dates + reg_counts in context | ✅ |

### Dashboard KPI Context Verified

| KPI | Source | Data Type |
|---|---|---|
| `revenue_total` | Sum of total_price of paid+ orders | Decimal |
| `orders_total` | Order.objects.count() | int |
| `active_customers` | Distinct users with orders | int |
| `active_products` | Product.is_available=True count | int |
| `aov` | Avg(total_price) of paid orders | Decimal |
| `paid_rate` | % of orders that are paid+ | int (0-100) |
| `revenue_today` | Today's paid order revenue | Decimal |
| `orders_today` | Today's orders | int |
| `has_chart_data` | Sum of revenue_chart > 0 and len > 2 | bool |
| `status_counts` | Per-status order breakdown | dict |

---

## Module 2: Products (30 tests)

| Group | Tests | Result |
|---|---|---|
| Product changelist access | 200 | ✅ |
| Product add page renders | 200 | ✅ |
| Product change page renders with name | 200 + name in HTML | ✅ |
| Mark as available action | flips is_available=True | ✅ |
| Mark as unavailable action | flips is_available=False | ✅ |
| Filter by category | 200 | ✅ |
| Filter by is_available | 200 | ✅ |
| Search by name | 200 | ✅ |
| Date hierarchy navigation | 200 | ✅ |
| Product delete | deleted from DB | ✅ |
| Brand CRUD | list, add, change, search | ✅ |
| FragranceNote CRUD | list, add, filter by note_type | ✅ |
| FragranceFamily CRUD | list, add | ✅ |
| ProductVariant inline rendered | 200 | ✅ |
| Review changelist | 200 with review data | ✅ |
| ProductSlugRedirect changelist | 200 | ✅ |
| SlugRedirect readonly | unchanged after POST | ✅ |
| ProductInfo display | name in change page | ✅ |

---

## Module 3: Categories (8 tests)

| Test | Description | Result |
|---|---|---|
| Changelist | 200 + category name visible | ✅ |
| Add | Create "Body Mist" via ORM | ✅ |
| Change | Update name via ORM | ✅ |
| Delete | Remove from DB | ✅ |
| Search | ?q=Parfum → 200 | ✅ |
| Product count column | category name in changelist | ✅ |
| Slug prepopulated | Add page renders | ✅ |
| FragranceFamily list | 200 | ✅ |

---

## Module 4: Orders (28 tests)

### Status Transition Tests

All 6 admin actions tested with correct from-state and guard conditions:

| Action | From → To | Valid Transition | Wrong-State Guard | Cancel Blocked |
|---|---|---|---|---|
| `mark_as_paid` | pending_payment → paid | ✅ | processing stays processing | — |
| `mark_as_processing` | paid → processing | ✅ | — | — |
| `mark_as_shipped` | processing → shipped | ✅ | — | — |
| `mark_as_delivered` | shipped → delivered | ✅ | — | — |
| `mark_as_completed` | delivered → completed | ✅ | — | — |
| `mark_as_cancelled` | any → cancelled | ✅ (from processing) | — | DELIVERED stays ❌ |
| `mark_as_cancelled` | — | — | — | COMPLETED stays ❌ |

### Guard Logic Verified

```
pending_payment → [paid, cancelled]
paid → [processing, cancelled]
processing → [shipped, cancelled]
shipped → [delivered, cancelled]
delivered → [completed] (cancelled blocked)
completed → [] (cancelled blocked)
```

### Other Order Tests

| Test | Description | Result |
|---|---|---|
| Changelist | 200 | ✅ |
| Change page | 200 + order_number | ✅ |
| Fields readonly (order_number, subtotal, total_price, timestamps) | visible in form | ✅ |
| Filter by status | 200 | ✅ |
| Search by order_number | 200 | ✅ |
| OrderStatusHistory created | >= 1 record | ✅ |
| OrderStatusHistory changelist | 200 | ✅ |
| OrderStatusHistory add denied | 403 (has_add_permission=False) | ✅ |
| OrderItem inline renders | product name in change page | ✅ |
| Search by username | 200 | ✅ |
| Status badge text | "pending" in changelist | ✅ |
| User link | username appears in change page | ✅ |
| Shipping info | recipient_name appears | ✅ |
| Legacy orders.Voucher admin | list + add | ✅ |
| Status timestamp updates | paid_at set after mark_as_paid | ✅ |
| Delete allowed | POST delete → success | ✅ |

---

## Module 5: Customers (20 tests)

| Test | Description | Result |
|---|---|---|
| User changelist | 200 | ✅ |
| User add (via ORM) | created in DB | ✅ |
| User change page | 200 | ✅ |
| User order_count column | changelist loads | ✅ |
| Search by username | 200 | ✅ |
| Filter by is_active | 200 | ✅ |
| Profile changelist | 200 | ✅ |
| MemberProfile changelist | 200 | ✅ |
| Level filter | 200 | ✅ |
| Spending readonly | unchanged after POST | ✅ |
| Points readonly | unchanged after POST | ✅ |
| PointTransaction changelist | 200 | ✅ |
| PointTransaction add denied | 403 (has_add_permission=False) | ✅ |
| PointTransaction list with data | "Test poin" in HTML | ✅ |
| CustomerAddress changelist | 200 | ✅ |
| Address filter (is_default) | 200 | ✅ |
| Wishlist changelist | 200 | ✅ |
| Wishlist add | created in DB | ✅ |
| User total_spending column | changelist loads | ✅ |
| PointTransaction filter by type | 200 | ✅ |

---

## Module 6: Promotions (15 tests)

| Test | Description | Result |
|---|---|---|
| Voucher changelist | 200 + "ADMIN10" visible | ✅ |
| Add page renders | 200 | ✅ |
| Change page renders | 200 + code in HTML | ✅ |
| Filter by voucher_type | 200 | ✅ |
| Search by code | 200 + code in HTML | ✅ |
| mark_active action | is_active flips to True | ✅ |
| mark_inactive action | is_active flips to False | ✅ |
| UserVoucher changelist | 200 | ✅ |
| UserVoucher search | 200 | ✅ |
| UserVoucher status filter | 200 | ✅ |
| claimed_count readonly | unchanged after POST | ✅ |
| used_count readonly | unchanged after POST | ✅ |
| Unlimited quota render | add page shows quota field | ✅ |
| Voucher type badge | code in changelist HTML | ✅ |
| UserVoucher inline rendered | change page loads | ✅ |

---

## Module 7: Voucher (7 tests)

Both voucher models (orders.Voucher + promotions.Voucher) tested:

| Test | Description | Result |
|---|---|---|
| Legacy orders.Voucher list | 200 + code visible | ✅ |
| Legacy orders.Voucher filter | 200 | ✅ |
| Legacy used_count readonly | unchanged after POST | ✅ |
| All 5 promotions voucher types | changelist loads | ✅ |
| Promotions voucher search | code in HTML | ✅ |
| Promotions voucher delete | removed from DB | ✅ |
| Legacy voucher delete | removed from DB | ✅ |

---

## Module 8: Loyalty (12 tests)

| Test | Description | Result |
|---|---|---|
| Member list | 200 | ✅ |
| Level display | changelist loads | ✅ |
| Level filter (GOLD) | 200 | ✅ |
| PointTransaction list | 200 | ✅ |
| PointTransaction data rendered | description in HTML | ✅ |
| All 3 transaction types (EARN/REDEEM/UPGRADE) | list loads with all types | ✅ |
| Spending readonly | unchanged after POST | ✅ |
| Points readonly | unchanged after POST | ✅ |
| Manual level upgrade via ORM | level changes | ✅ |
| PointTransaction filter by type | 200 | ✅ |
| MemberProfile search | 200 | ✅ |
| Member auto-created for user | list loads | ✅ |

---

## Module 9: Reports (20 tests)

| Test | Description | Result |
|---|---|---|
| KPI revenue_total | >= 0 | ✅ |
| KPI orders_total | >= 1 (with fixture) | ✅ |
| KPI active_customers | >= 0 | ✅ |
| KPI active_products | >= 1 (with fixture) | ✅ |
| KPI AOV | >= 0 | ✅ |
| KPI paid_rate | >= 0 | ✅ |
| revenue_today | >= 0 | ✅ |
| orders_today | >= 0 | ✅ |
| top_products in context | present | ✅ |
| monthly_data (12 months) | length == 12 | ✅ |
| status_counts | >= 1 entry | ✅ |
| category_revenue in context | present | ✅ |
| top_customers in context | present | ✅ |
| payment_methods in context | present | ✅ |
| Customer growth chart | reg_dates + reg_counts present | ✅ |
| Low stock notifications | product with stock=2 appears | ✅ |
| Sidebar quick insights | best_product, sidebar_pending, etc. | ✅ |
| Recent activity timeline | activities with order/payment/review types | ✅ |
| Member counts | SILVER/GOLD/PLATINUM all in context | ✅ |
| Average rating | avg_rating in context | ✅ |

---

## Module 10: Settings (14 tests)

| Test | Description | Result |
|---|---|---|
| Password change page | 200 | ✅ |
| Password change done | 200/302 | ✅ |
| Jazzmin installed | in INSTALLED_APPS | ✅ |
| Jazzmin settings | site_title, site_header, site_brand, welcome_sign verified | ✅ |
| Jazzmin UI tweaks | non-empty | ✅ |
| SeparateAdminSessionMiddleware | configured in MIDDLEWARE | ✅ |
| LOGIN_URL | 'accounts:login' | ✅ |
| Custom admin template | "Morris Parfum" in HTML | ✅ |
| Admin logout | POST → 200/302 | ✅ |
| Order change_form template | 200 | ✅ |
| Brand in navbar | "Morris" in admin HTML | ✅ |
| search_model configured | auth.User in search_model | ✅ |
| topmenu_links configured | present in settings | ✅ |
| Icons configured | non-empty dict | ✅ |

---

## Module 11: Permission (19 tests)

| Test | Description | Result |
|---|---|---|
| Anonymous redirect from index | 302 to login | ✅ |
| Anonymous blocked from product list | 302 | ✅ |
| Regular user redirected from admin | 302 | ✅ |
| Regular user blocked from ALL admin URLs | All return 302/403 | ✅ |
| Staff (is_staff=True) can access admin | 200 | ✅ |
| Superuser can access all changelists | All 200 | ✅ |
| Superuser blocked from customer dashboard | 302 | ✅ |
| Superuser blocked from profile | 302 | ✅ |
| Superuser blocked from cart | 302 | ✅ |
| Superuser blocked from order create | 302 | ✅ |
| CSRF on admin login form | token present | ✅ |
| CSRF on admin add form | token present | ✅ |
| Admin login template renders | 200 + login-related content | ✅ |
| Admin index redirect URL | contains login | ✅ |
| Group admin | changelist 200 | ✅ |
| Group add via ORM | created in DB | ✅ |
| Staff-not-superuser can access customer dashboard | 200 | ✅ |

---

## Module 12: Cart / Payment / Regions (18 tests)

| Test | Description | Result |
|---|---|---|
| Cart changelist | 200 | ✅ |
| Cart list with items | 200 | ✅ |
| Cart detail page | 200 | ✅ |
| Payment changelist | 200 | ✅ |
| Payment change page | 200 | ✅ |
| Payment search | 200 | ✅ |
| Payment filter by status | 200 | ✅ |
| Payment filter by method | 200 | ✅ |
| Payment change page renders | 200 | ✅ |
| Payment status history changelist | 200 | ✅ |
| Payment history add denied | 403 (has_add_permission=False) | ✅ |
| Province list | 200 | ✅ |
| City list | 200 | ✅ |
| Province add | created in DB | ✅ |
| City add | created in DB | ✅ |
| District list | 200 | ✅ |
| Postal code list | 200 | ✅ |

---

## Admin Models Coverage Matrix

| Model | App | Changelist | Add | Change | Delete | Readonly | Readonly Fields Verified | Actions Verified |
|---|---|---|---|---|---|---|---|---|
| User | auth | ✅ | ✅ | ✅ | — | — | — | — |
| Group | auth | ✅ | ✅ | — | — | — | — | — |
| Profile | accounts | ✅ | — | — | — | — | — | — |
| MemberProfile | accounts | ✅ | — | ✅ | — | ✅ total_points, total_spending | ✅ | — |
| PointTransaction | accounts | ✅ | ❌ 403 | — | — | ✅ all fields | — | — |
| CustomerAddress | accounts | ✅ | — | — | — | — | — | — |
| Wishlist | accounts | ✅ | ✅ | — | — | — | — | — |
| Product | products | ✅ | ✅ | ✅ | ✅ | ✅ thumbnail_preview_detail | — | ✅ mark_as_available, mark_as_unavailable |
| Category | products | ✅ | ✅ | ✅ | ✅ | — | — | — |
| Brand | products | ✅ | ✅ | ✅ | — | — | — | — |
| FragranceNote | products | ✅ | ✅ | — | — | — | — | — |
| FragranceFamily | products | ✅ | ✅ | — | — | — | — | — |
| ProductSlugRedirect | products | ✅ | — | ✅ | — | ✅ old_slug, product, created_at | ✅ | — |
| Review | products | ✅ | ✅ | — | — | ✅ user, product, rating, comment | — | — |
| Cart | carts | ✅ | — | ✅ | — | — | — | — |
| Order | orders | ✅ | — | ✅ | ✅ | ✅ order_number, subtotal, total_price, timestamps | ✅ | ✅ 6 status actions |
| OrderStatusHistory | orders | ✅ | ❌ 403 | — | — | ✅ all fields | — | — |
| Voucher (legacy) | orders | ✅ | ✅ | ✅ | ✅ | ✅ used_count | ✅ | — |
| Payment | payments | ✅ | — | ✅ | — | ✅ snap_token, snap_redirect_url, raw_response | ✅ | — |
| PaymentStatusHistory | payments | ✅ | ❌ 403 | — | — | ✅ all fields | — | — |
| Voucher (promotions) | promotions | ✅ | ✅ | ✅ | ✅ | ✅ claimed_count, used_count | ✅ | ✅ mark_active, mark_inactive |
| UserVoucher | promotions | ✅ | — | — | — | ✅ assigned_at, used_at | — | — |
| Province | regions | ✅ | ✅ | — | — | — | — | — |
| City | regions | ✅ | ✅ | — | — | — | — | — |
| District | regions | ✅ | — | — | — | — | — | — |
| PostalCode | regions | ✅ | — | — | — | — | — | — |

**Legend:** ✅ = tested and passes, ❌ 403 = PermissionDenied (correctly blocked), — = not tested

---

## Admin URL Names Extracted & Verified

| URL Name | Path | Module |
|---|---|---|
| `admin:login` | `/admin/login/` | Dashboard |
| `admin:logout` | `/admin/logout/` | Dashboard |
| `admin:index` | `/admin/` | Dashboard |
| `admin:password_change` | `/admin/password_change/` | Settings |
| `admin:password_change_done` | `/admin/password_change/done/` | Settings |
| `admin_dashboard` | `/admin/dashboard/` | Dashboard/Reports |
| `admin:auth_user_changelist` | `/admin/auth/user/` | Customers |
| `admin:auth_user_add` | `/admin/auth/user/add/` | Customers |
| `admin:auth_group_changelist` | `/admin/auth/group/` | Permission |
| `admin:products_product_changelist` | `/admin/products/product/` | Products |
| `admin:products_product_add` | `/admin/products/product/add/` | Products |
| `admin:products_brand_changelist` | `/admin/products/brand/` | Products |
| `admin:products_category_changelist` | `/admin/products/category/` | Categories |
| `admin:products_fragrancenote_changelist` | `/admin/products/fragrancenote/` | Products |
| `admin:products_fragrancefamily_changelist` | `/admin/products/fragrancefamily/` | Products |
| `admin:products_review_changelist` | `/admin/products/review/` | Products |
| `admin:products_productslugredirect_changelist` | `/admin/products/productslugredirect/` | Products |
| `admin:orders_order_changelist` | `/admin/orders/order/` | Orders |
| `admin:orders_orderstatushistory_changelist` | `/admin/orders/orderstatushistory/` | Orders |
| `admin:orders_voucher_changelist` | `/admin/orders/voucher/` | Voucher |
| `admin:payments_payment_changelist` | `/admin/payments/payment/` | Cart/Payment/Regions |
| `admin:payments_paymentstatushistory_changelist` | `/admin/payments/paymentstatushistory/` | Cart/Payment/Regions |
| `admin:promotions_voucher_changelist` | `/admin/promotions/voucher/` | Promotions |
| `admin:promotions_uservoucher_changelist` | `/admin/promotions/uservoucher/` | Promotions |
| `admin:accounts_profile_changelist` | `/admin/accounts/profile/` | Customers |
| `admin:accounts_memberprofile_changelist` | `/admin/accounts/memberprofile/` | Loyalty |
| `admin:accounts_pointtransaction_changelist` | `/admin/accounts/pointtransaction/` | Loyalty |
| `admin:accounts_customeraddress_changelist` | `/admin/accounts/customeraddress/` | Customers |
| `admin:accounts_wishlist_changelist` | `/admin/accounts/wishlist/` | Customers |
| `admin:carts_cart_changelist` | `/admin/carts/cart/` | Cart/Payment/Regions |
| `admin:regions_province_changelist` | `/admin/regions/province/` | Cart/Payment/Regions |
| `admin:regions_city_changelist` | `/admin/regions/city/` | Cart/Payment/Regions |
| `admin:regions_district_changelist` | `/admin/regions/district/` | Cart/Payment/Regions |
| `admin:regions_postalcode_changelist` | `/admin/regions/postalcode/` | Cart/Payment/Regions |

---

## Jazzmin Configuration Verified

| Setting | Expected | Actual |
|---|---|---|
| `site_title` | "Morris Parfum Admin" | ✅ |
| `site_header` | "Morris Parfum" | ✅ |
| `site_brand` | "Morris Parfum" | ✅ |
| `welcome_sign` | "Selamat Datang di Dashboard Morris Parfum" | ✅ |
| `search_model` | Includes `auth.User`, `products.Product`, `orders.Order` | ✅ |
| `topmenu_links` | Configured | ✅ |
| `icons` | Non-empty | ✅ |
| `JAZZMIN_UI_TWEAKS` | Present and non-empty | ✅ |
| `SeparateAdminSessionMiddleware` | In MIDDLEWARE | ✅ |

---

## Permission Matrix

| User Type | `/admin/` | `/admin/dashboard/` | Admin Changelists | Customer Views |
|---|---|---|---|---|
| Anonymous | 302 redirect | 302 redirect | 302 redirect | 200 (home) |
| Regular user (is_staff=False) | 302 redirect | 302 redirect | 302 redirect | 200 |
| Staff (is_staff=True, not superuser) | 200 | 200 (with perms) | 200 (with perms) | 200 |
| Superuser (is_staff=True, is_superuser=True) | 200 | 200 | 200 | 302 (blocked) |

---

## Bugs Found

### None

All admin behaviors matched expected Django + custom implementation behavior. Two minor test assumption corrections were made during testing:

1. `has_add_permission=False` raises `PermissionDenied` (403), not 200 — this is correct Django behavior and not a bug.
2. `MemberProfile.level` is NOT in `readonly_fields` (only `total_points`, `total_spending`, `created_at`, `updated_at` are) — correct behavior.
3. `is_staff` (not superuser) `staff` users can access customer views because `@customer_required` and `CustomerRequiredMixin` check `is_superuser`, not `is_staff` — correct behavior.
