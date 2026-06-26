# Pricing Model Draft

Goal: create a clear pricing model for the ROS2-Compatible STM32 Robot Controller Kit before listing it on Tindie or Shopify.

> Validation status: draft. Do not publish a final price until BOM, PCB, assembly, packaging, payment fees, platform fees, defect reserve, and shipping quotes are verified.

## Pricing Rule

Do not price from gut feeling.

Use this chain:

```text
Unit manufacturing cost
  + packaging cost
  + factory test cost
  + payment fee
  + platform fee
  + defect / replacement reserve
  + support reserve
  + shipping subsidy, if any
  + target profit
  = selling price
```

## First-Stage Sales Assumption

First sales channel:

```text
Tindie + PayPal, small tested batch
```

Reason:

- Tindie is suitable for small-batch developer hardware.
- PayPal is commonly supported for early cross-border hardware sales.
- Shopify and Stripe can wait until product demand and fulfillment are more stable.

## Required Inputs

Fill these before publishing any price.

| Input | Unit | Current Value | Status | Notes |
| --- | --- | --- | --- | --- |
| PCB fabrication cost | USD / board | TBD | Need quote | Include tooling or setup if any |
| SMT assembly cost | USD / board | TBD | Need quote | Include small-batch premium |
| Component BOM cost | USD / board | TBD | Need BOM | Use MPN-based BOM, not only Taobao names |
| Firmware flashing cost | USD / unit | TBD | Need process | Can be labor time or fixture amortization |
| Factory test cost | USD / unit | TBD | Need process | Include test time and failed units |
| Cable set cost | USD / kit | TBD | Need supplier | Include all included cables |
| Packaging cost | USD / kit | TBD | Need supplier | Anti-static bag, box, label, card |
| Documentation card cost | USD / kit | TBD | Need quote | Optional QR code card |
| Defect reserve | % of selling price | TBD | Need policy | Covers replacement and bad units |
| Support reserve | USD / kit | TBD | Need estimate | Support time is real cost |
| Platform fee | % of selling price | TBD | Verify | Tindie / Shopify differs |
| Payment fee | % + fixed fee | TBD | Verify | PayPal / Stripe differs by account and country |
| Currency buffer | % of selling price | TBD | Need policy | Protects against exchange movement |
| Target gross margin | % of selling price | TBD | Need decision | Must fund iteration, not just survival |

## Formula

Definitions:

```text
UnitVariableCost =
  PCB
  + Assembly
  + BOM
  + FirmwareFlashing
  + FactoryTest
  + CableSet
  + Packaging
  + DocumentationCard
  + SupportReserve
  + ShippingSubsidy

PercentageCostRate =
  PlatformFeeRate
  + PaymentFeeRate
  + DefectReserveRate
  + CurrencyBufferRate
  + TargetGrossMarginRate

MinimumSellingPrice =
  (UnitVariableCost + FixedPaymentFee) / (1 - PercentageCostRate)
```

Important:

- If `PercentageCostRate` is too high, the product price becomes impossible.
- If shipping is charged separately, do not include full shipping in `UnitVariableCost`.
- If shipping is partially subsidized, include only the subsidy.
- If the customer pays shipping fully, shipping margin should still be checked in `shipping_matrix.csv`.

## Example Worksheet

This is an example only. Replace every value before listing.

| Item | Example USD | Notes |
| --- | ---: | --- |
| PCB fabrication | 3.00 | Placeholder |
| Assembly | 5.00 | Placeholder |
| BOM | 18.00 | Placeholder |
| Firmware flashing | 1.00 | Placeholder |
| Factory test | 2.00 | Placeholder |
| Cable set | 2.00 | Placeholder |
| Packaging | 2.00 | Placeholder |
| Documentation card | 0.50 | Placeholder |
| Support reserve | 3.00 | Placeholder |
| Shipping subsidy | 0.00 | Charge shipping separately in first batch |
| Unit variable cost | 36.50 | Sum of above |
| Platform fee rate | 5.0% | Verify before listing |
| Payment fee rate | 5.0% | Verify before listing |
| Defect reserve rate | 5.0% | Placeholder |
| Currency buffer rate | 3.0% | Placeholder |
| Target gross margin rate | 35.0% | Placeholder |
| Fixed payment fee | 0.50 | Verify before listing |
| Minimum selling price | 77.66 | Example formula result |

Example formula:

```text
(36.50 + 0.50) / (1 - 0.05 - 0.05 - 0.05 - 0.03 - 0.35) = 77.66
```

Do not treat this as the final price. It only shows how sensitive the price is to hidden costs.

## Recommended First-Batch Policy

For the first small batch:

- Charge product price and shipping separately.
- Do not offer free worldwide shipping.
- Start with fewer shipping countries.
- Use tracked shipping where possible.
- Keep 3 to 10 units as the first batch.
- Keep at least one replacement unit aside.
- Do not discount before true cost is known.

## Price Bands To Test

Use these as research bands, not final prices.

| Price Band | Meaning |
| --- | --- |
| USD 39 to 49 | Likely too low unless BOM and fulfillment are very lean |
| USD 59 to 79 | Possible educational / maker kit range |
| USD 89 to 129 | Possible if docs, ROS2 package, support, and test quality are strong |
| USD 149+ | Needs strong proof, real demo, reliable hardware, and clear differentiation |

## Listing Decision Checklist

Do not publish the listing until:

- [ ] BOM cost is known.
- [ ] Assembly cost is known.
- [ ] Packaging cost is known.
- [ ] Payment fee is verified.
- [ ] Platform fee is verified.
- [ ] Shipping matrix is filled for target countries.
- [ ] Return policy is clear.
- [ ] Factory test process exists.
- [ ] At least one full demo proves the kit works.
- [ ] The product page does not claim CE or FCC certification.

## Open Questions

- [ ] Should motor driver be onboard or external in the first sellable kit?
- [ ] Is the kit sold as board-only or board plus cable set?
- [ ] Is shipping charged separately by country?
- [ ] Is there a beta discount for first users?
- [ ] How much support time can be afforded per customer?
- [ ] What is the minimum acceptable gross margin after all fees?

