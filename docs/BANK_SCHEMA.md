# Bank JSON Schema

Import format for question banks. In-app: Home → Import bank → select JSON
file. Validation is atomic: a bank is rejected as a whole if ANY question
fails, with a per-question error list.

## Shape

```json
{
  "name": "PYQ Physics 2016-2020",
  "source": "NTA NEET official PYQs",
  "questions": [
    {
      "subject": "Physics",
      "chapter": "Mechanics",
      "q": "A body starts from rest and moves with uniform acceleration a. Distance covered in the nth second is:",
      "opts": [
        "u + a(2n-1)/2",
        "u + a(2n+1)/2",
        "a(2n-1)/2",
        "u + a(n-1)/2"
      ],
      "ans": 2,
      "expl": "s_n = u + a(2n-1)/2; u=0 so a(2n-1)/2."
    }
  ]
}
```

## Fields

| field       | required | rule                                          |
|-------------|----------|-----------------------------------------------|
| name        | yes      | non-empty string                              |
| source      | no       | attribution string, shown on test start       |
| questions   | yes      | array, 1..1000                                |
| .subject    | yes      | one of: Physics, Chemistry, Botany, Zoology   |
| .chapter    | no       | string, shown as tag                          |
| .q          | yes      | non-empty string, unique within bank          |
| .opts       | yes      | array of exactly 4 non-empty strings          |
| .ans        | yes      | integer 0-3 (index of correct option)         |
| .expl       | no       | explanation string, shown in review           |

## Validation rules

- subject must be exactly one of the 4 enum values (case-sensitive).
- opts length == 4, every option non-empty.
- ans integer in [0,3].
- duplicate q text within a bank → rejected.
- UTF-8 JSON only. Plain text (HTML sub/sup allowed for math like
  `H<sub>2</sub>O`, `10<sup>-6</sup>`).

## Notes

- Sample banks from the app export in this same format — export one to
  use as a template.
- Keep banks ≤ ~1000 questions for smooth performance on phones.
