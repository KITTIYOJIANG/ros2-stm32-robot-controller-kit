# Fulfillment SOP

Goal: define a repeatable order fulfillment workflow for small-batch overseas sales of the ROS2-Compatible STM32 Robot Controller Kit.

> Validation status: draft SOP. Do not use this as a live fulfillment policy until the factory test script, packaging materials, shipping labels, and support process are validated.

## Scope

This SOP covers the first small-batch sales workflow:

```text
Order received
  -> order review
  -> board test
  -> evidence capture
  -> packaging
  -> shipping label
  -> tracking update
  -> customer notification
  -> support record
```

Target batch size:

```text
3 to 10 tested developer kits
```

## Roles

For the first batch, one person may do all roles. Still keep the roles separate on paper so the process is auditable.

| Role | Responsibility |
| --- | --- |
| Order reviewer | Check order, country, address, payment, and fraud risk |
| Test operator | Run factory test and save log |
| Packing operator | Pack unit and take photos |
| Shipping operator | Create label and upload tracking |
| Support owner | Handle post-shipment questions and issues |

## Required Materials

Before accepting orders:

- [ ] Tested robot controller boards
- [ ] Cable sets, if included
- [ ] Anti-static bags
- [ ] Protective boxes or padded mailers
- [ ] Quick Start card or QR code card
- [ ] Product label with board revision and firmware version
- [ ] Shipping labels
- [ ] Scale for packed weight
- [ ] Camera or phone for evidence photos
- [ ] Factory test script
- [ ] Test log folder

## Folder Structure For Evidence

Use one folder per order.

```text
ops/factory_test_log/
  ORDER-0001/
    order_summary.md
    factory_test.log
    board_top.jpg
    board_bottom.jpg
    package_contents.jpg
    packed_box.jpg
    shipping_label_redacted.jpg
```

Do not commit private customer information to the public GitHub repository. Keep public examples anonymized or use fake sample data.

## Step 1: Order Review

Checklist:

- [ ] Confirm payment is received.
- [ ] Confirm destination country is enabled in `store/shipping_matrix.csv`.
- [ ] Confirm customer paid the correct shipping amount.
- [ ] Confirm address looks complete.
- [ ] Confirm product is in stock.
- [ ] Confirm this is not a preorder unless clearly labeled as preorder.
- [ ] Confirm buyer expectations match developer-kit status.

Block the order if:

- Destination country is marked `Block until verified`.
- Shipping cost is unknown or obviously undercharged.
- Address is incomplete.
- The product is not tested stock.
- Buyer expects certified consumer or industrial hardware.

## Step 2: Prepare Test Station

Test station should include:

- Host computer
- USB cable
- ST-Link or supported programmer
- Current-limited power supply
- Known-good motor or dummy load
- Known-good IMU or sensor module
- Known-good encoder signal source, if available
- Camera or phone

Pre-test checks:

- [ ] Desk is clear.
- [ ] Board is visually inspected.
- [ ] No loose metal objects near powered electronics.
- [ ] Motor wheels or shafts cannot move dangerously.
- [ ] Power supply voltage and current limit are set correctly.

## Step 3: Visual Inspection

Inspect and record:

- [ ] Board revision label
- [ ] Solder bridges
- [ ] Damaged connector
- [ ] Missing component
- [ ] Bent pin
- [ ] Scratched PCB
- [ ] Loose cable

Photo evidence:

- [ ] Top side of board
- [ ] Bottom side of board
- [ ] Board revision or label

## Step 4: Flash Firmware

Planned command:

```bash
cd firmware
make flash
```

Record:

```text
Firmware version:
Git commit:
Flash result:
Operator:
Date:
```

Pass criteria:

- [ ] Programmer connects.
- [ ] Flash completes.
- [ ] Verify step passes.
- [ ] Firmware version can be queried.

Fail action:

- Do not ship.
- Save test log.
- Mark unit as failed.
- Diagnose separately from sellable stock.

## Step 5: Factory Test

Planned command:

```bash
python tools/factory_test.py --port /dev/ttyUSB0 --order ORDER-0001
```

Minimum tests:

- [ ] Query firmware version.
- [ ] Query board status.
- [ ] Confirm `ERR_OK`.
- [ ] Run motor stop command.
- [ ] Run low-speed motor command with safe setup.
- [ ] Read IMU data.
- [ ] Read encoder count or simulated encoder input.
- [ ] Confirm command timeout stops motors.
- [ ] Confirm diagnostics heartbeat.

Pass criteria:

```text
All required tests pass.
No motor fault.
No sensor fault.
No firmware version mismatch.
Command timeout behavior verified.
```

Fail action:

- Do not ship.
- Move unit to failed inventory.
- Record failure reason.
- Rework only if root cause is understood.

## Step 6: Create Order Summary

Create `order_summary.md` in the private order folder.

Template:

```markdown
# Order Summary

Order ID:
Order Date:
Destination Country:
Product:
Board Revision:
Firmware Version:
Factory Test Result:
Packed Weight:
Shipping Provider:
Tracking Number:
Operator:
Notes:
```

Do not commit real names, addresses, phone numbers, emails, or tracking numbers to the public repository.

## Step 7: Pack The Kit

Packing checklist:

- [ ] Put tested board in anti-static bag.
- [ ] Add cable set, if included.
- [ ] Add Quick Start card or QR code card.
- [ ] Add warning note: developer kit, lab use only.
- [ ] Add packing protection.
- [ ] Put everything into box or padded mailer.
- [ ] Weigh packed parcel.
- [ ] Record packed weight.

Photo evidence:

- [ ] Package contents before sealing
- [ ] Sealed package
- [ ] Shipping label with private data redacted for records

## Step 8: Create Shipping Label

Before buying label:

- [ ] Confirm destination country is enabled.
- [ ] Confirm customer shipping payment covers cost.
- [ ] Confirm tracking is available if promised.
- [ ] Confirm customs description is accurate.
- [ ] Confirm declared value matches store policy.

Draft customs description:

```text
Educational robot controller development board
```

Do not write misleading customs descriptions.

## Step 9: Upload Tracking And Notify Customer

Customer notification should include:

- Tracking number
- Carrier
- Documentation link
- Support channel
- Reminder that it is a developer kit for safe lab use

Draft message:

```text
Your ROS2-Compatible STM32 Robot Controller Kit has shipped.

Carrier:
Tracking:
Documentation:
Quick Start:
Support:

Please use the kit in a safe lab environment and review the Quick Start before connecting motor power.
```

## Step 10: Post-Shipment Support

Support log should track:

- [ ] Customer issue
- [ ] Firmware version
- [ ] Host OS
- [ ] Serial port
- [ ] Error message
- [ ] Photos requested
- [ ] Resolution
- [ ] Documentation update needed

If a question repeats, update:

- [ ] `docs/troubleshooting.md`
- [ ] `docs/faq.md`
- [ ] `docs/quick_start.md`

## Replacement Or Return Review

Before replacing a unit:

- [ ] Check factory test log.
- [ ] Ask for wiring photos.
- [ ] Ask for firmware version.
- [ ] Ask for power supply voltage.
- [ ] Confirm issue is not caused by incorrect wiring, over-voltage, short circuit, or unsupported setup.

Possible outcomes:

- Setup support
- Documentation update
- Firmware fix
- Replacement
- Refund
- Return denied due to misuse

## Public Release Safety Rules

- Do not claim CE or FCC certification before certification is complete.
- Do not sell untested boards.
- Do not promise shipping timelines before real fulfillment is tested.
- Do not offer free worldwide shipping without real cost data.
- Do not hide known hardware or firmware defects.
- Do not ship units that fail factory test.

## First Batch Exit Criteria

Before opening public stock:

- [ ] Factory test script exists.
- [ ] At least 3 units pass factory test.
- [ ] Each unit has photo evidence.
- [ ] Shipping matrix has verified countries and costs.
- [ ] Packaging material is ready.
- [ ] Support channel is ready.
- [ ] Quick Start is usable.
- [ ] Troubleshooting covers known bring-up issues.
- [ ] Tindie listing clearly says developer kit.
- [ ] Replacement reserve exists.

## Draft Gaps

- [ ] Create `tools/factory_test.py`.
- [ ] Create private order log template outside public repo.
- [ ] Confirm shipping provider.
- [ ] Confirm customs description and HS code.
- [ ] Confirm support email or GitHub issue process.
- [ ] Confirm exact package weight.
- [ ] Add packing photos after first sample package.

