# AI Coding Principles

**Goal:** Write code that another developer (or AI) can understand, modify, and review quickly without additional explanation. Keep outputs concise, focused, and strictly aligned with the requested specifications.

## 1. Keep solutions simple.

✅ Use straightforward logic that is easy to follow.
❌ Avoid clever one-liners, deep abstractions, or premature optimization.

- **Example:** Use a standard `for` loop or `.filter()` to process an array instead of a deeply nested, chained `.reduce()` that is difficult to parse at a glance.

## 2. Use meaningful names.

✅ `customer_count`, `retry_attempts`, `fetch_user_profile()`
❌ `x`, `data`, `temp`, `func()`

- **Example:** Instead of `const d = arr.filter(x => x.a);`, write `const activeUsers = users.filter(user => user.isActive);`.

## 3. Write self-explanatory code.

✅ Code should be understandable from structure and naming.
❌ Relying on comments to explain confusing code.

- **Example:** Extract complex boolean logic into a clearly named variable, like `const isEligibleForDiscount = userAge > 65 && hasMembership;`, rather than leaving a comment like `// check if they get a discount` above an obscure `if` statement.

## 4. Prefer readability over cleverness.

✅ Explicit conditions and clear control flow.
❌ Dense expressions that save lines but hurt understanding.

- **Example:** Use standard `if/else` blocks rather than chaining multiple ternary operators (`a ? b : c ? d : e`), which saves space but destroys readability.

## 5. Keep functions focused (Single Responsibility).

✅ One function, one responsibility.
❌ Functions that validate, transform, save, log, and notify at once.

- **Example:** Create three separate functions—`parseData()`, `validateData()`, and `saveData()`—instead of writing one giant 200-line `processEverything()` function.

## 6. Follow existing project conventions.

✅ Match the project's patterns, structure, and style.
❌ Introducing a new pattern for every feature.

- **Example:** If an existing React project relies exclusively on Functional Components and Hooks, do not introduce a Class Component for a new feature just because it is technically valid.

## 7. Use types and handle errors explicitly.

✅ Validate inputs and fail with clear error messages.
❌ Silent failures, broad catches, or excessive use of `any`.

- **Example:** In TypeScript, define a strict interface (`interface User { id: number; name: string }`) instead of typing a payload as `data: any`. Catch specific API errors and throw descriptive messages rather than using an empty `catch (e) {}` block that swallows the error.

## 8. Avoid unnecessary code (YAGNI).

✅ Add only what is needed today.
❌ Unused abstractions, dependencies, comments, emojis, dead code, or speculative features.

- **Example:** Do not build a complex, generic caching layer for a database query if that query is currently only executed once a day. Stick to the immediate requirement.

## 9. Strictly adhere to the provided implementation plan.

✅ Implement exactly 'X' in 'Y' structure as requested.
❌ Guessing future needs, hallucwinating features, or adding speculative logic that enlarges the codebase unnecessarily.

- **Example:** If asked to write a function that "calculates total price," return just the mathematical sum. Do not proactively add discount logic, tax calculation APIs, or currency formatting wrappers unless they were explicitly requested in the plan.

## 10. Learn from well-maintained open-source projects.

✅ Study and adapt patterns from the most respected repositories in your current tech stack.
❌ Reinventing the wheel with non-standard folder structures or architectural paradigms.

- **Example:** If building a React application, observe how libraries like `React Query` or `Radix UI` structure their internal hooks and component props to inform your own design choices.
