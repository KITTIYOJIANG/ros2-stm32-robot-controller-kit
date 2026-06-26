# Shipping And Returns

Goal: define a clear draft policy for shipping, fulfillment, returns, and support before the first small-batch overseas sale.

> Validation status: draft policy. Shipping regions, carriers, delivery windows, prices, taxes, and return rules must be confirmed before listing the product for sale.

## Current Sales Status

The kit is not available for purchase yet.

First public sales target:

```text
Small-batch developer kits through Tindie after hardware validation.
```

Do not present prototypes as ready stock before they pass firmware, hardware, factory test, documentation, and fulfillment checks.

## Shipping Plan

Draft first-stage plan:

- Sell only a small tested batch.
- Ship only to countries where cost and tracking are understood.
- Use tracked shipping when possible.
- Avoid promising delivery windows before testing real fulfillment.
- Keep packaging simple, protective, and repeatable.

## Shipping Matrix

The shipping matrix will track real cost by country.

Target file:

```text
store/shipping_matrix.csv
```

Fields:

| Field | Purpose |
| --- | --- |
| Country | Destination country |
| Shipping Provider | Carrier or platform shipping option |
| Weight | Packed kit weight |
| Shipping Cost | Actual cost |
| Estimated Delivery Time | Conservative delivery range |
| Tracking Available | Yes or No |
| Risk Level | Low, Medium, High |
| Recommended Price | Shipping price to charge |
| Notes | Customs, delays, restrictions |

## Handling Time

Draft handling time:

```text
Ships after each unit passes factory test and packing inspection.
```

Do not promise same-day or next-day shipping until the workflow is tested.

## Fulfillment Checklist

Before shipping each unit:

- [ ] Confirm order details.
- [ ] Run factory test.
- [ ] Save test log.
- [ ] Photograph tested board.
- [ ] Pack in anti-static bag.
- [ ] Add quick start card or documentation link.
- [ ] Use protective packaging.
- [ ] Print and attach shipping label.
- [ ] Upload tracking number.
- [ ] Send shipping notification.

## Return Policy Draft

Final return rules are not set yet.

Draft principles:

- Be clear that the product is a developer kit.
- Do not accept returns for damage caused by incorrect wiring, over-voltage, short circuits, or unsafe lab setup.
- Offer support for setup issues through documentation and GitHub issues.
- Define a limited return or replacement window only after cost and logistics are understood.
- Keep photos and factory test logs for every shipped board.

## Damaged Or Defective Unit

If a buyer reports a defective unit, ask for:

- Order number
- Board revision
- Firmware version
- Photos of wiring
- Power supply voltage
- Exact failure symptom
- Terminal logs
- Whether the board passed power-on and flashing checks

Decision path:

1. Check whether the issue is setup-related.
2. Check whether the issue matches a known firmware or documentation bug.
3. Check factory test log for that unit.
4. Decide support, replacement, partial refund, or return after evidence review.

## Customs, Duties, And Taxes

Draft policy:

```text
Buyer is responsible for import duties, taxes, VAT, customs fees, and local handling charges unless the final store platform states otherwise.
```

This must be rewritten to match the final selling platform and target countries.

## Packaging Requirements

Minimum packaging target:

- Anti-static bag
- Protective box or padded mailer
- Quick Start link card
- Label with board revision and firmware version
- Optional QR code to GitHub documentation

## Support Boundary

Supported:

- Firmware flashing help
- SDK setup help
- ROS2 demo setup help
- Basic wiring clarification
- Troubleshooting known errors

Not guaranteed:

- Custom robot integration
- Third-party motor driver debugging beyond documented signals
- Damage caused by unsafe wiring or incorrect voltage
- Certified industrial deployment support

## Draft Gaps

- [ ] Confirm shipping countries
- [ ] Confirm shipping provider
- [ ] Confirm packed weight
- [ ] Confirm shipping prices
- [ ] Confirm return window
- [ ] Create factory test log template
- [ ] Create support email or issue template
- [ ] Add final store policy text

