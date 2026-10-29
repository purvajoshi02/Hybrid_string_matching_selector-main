
import time
from collections import Counter

import streamlit as st


# --------------------------------------------------
# ALGORITHM 1: NAIVE STRING MATCHING
# --------------------------------------------------

def naive_search(text, pattern):
    positions = []
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return positions

    for i in range(n - m + 1):
        j = 0

        while j < m and text[i + j] == pattern[j]:
            j += 1

        if j == m:
            positions.append(i)

    return positions


# --------------------------------------------------
# ALGORITHM 2: KMP STRING MATCHING
# --------------------------------------------------

def build_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    positions = []
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return positions

    lps = build_lps(pattern)

    i = 0
    j = 0

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j > 0:
                j = lps[j - 1]
            else:
                i += 1

    return positions


# --------------------------------------------------
# ALGORITHM 3: BOYER-MOORE (BAD-CHARACTER RULE)
# --------------------------------------------------

def boyer_moore_search(text, pattern):
    positions = []
    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return positions

    # Store the last occurrence of each pattern character.
    last = {}

    for i, char in enumerate(pattern):
        last[char] = i

    shift = 0

    while shift <= n - m:
        j = m - 1

        # Compare from right to left.
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            positions.append(shift)

            # Move safely to allow overlapping matches.
            if shift + m < n:
                shift += max(
                    1, m - last.get(text[shift + m], -1)
                )
            else:
                shift += 1
        else:
            shift += max(
                1, j - last.get(text[shift + j], -1)
            )

    return positions


# --------------------------------------------------
# ANALYZE INPUT AND SELECT AN ALGORITHM
# --------------------------------------------------

def analyze_input(text, pattern):
    counts = Counter(text)
    total_chars = len(text)

    # Fraction of characters that belong to the
    # most frequent character in the text.
    repetition = (
        max(counts.values()) / total_chars
        if total_chars > 0
        else 0
    )

    distinct_pattern_chars = len(set(pattern))
    pattern_length = len(pattern)
    text_length = len(text)

    # Simple, explainable selection rules.
    if text_length <= 1000 or pattern_length <= 3:
        algorithm = "Naive"
        reason = (
            "The text is small or the pattern is very short. "
            "The simple algorithm is a reasonable starting point."
        )

    elif repetition >= 0.50 or distinct_pattern_chars <= 2:
        algorithm = "KMP"
        reason = (
            "The text is highly repetitive or the pattern uses "
            "very few distinct characters. KMP avoids repeated "
            "comparisons using its LPS table."
        )

    elif pattern_length >= 8 and distinct_pattern_chars >= 6:
        algorithm = "Boyer-Moore"
        reason = (
            "The pattern is relatively long and has a varied "
            "alphabet. Boyer-Moore can skip sections of text."
        )

    else:
        algorithm = "KMP"
        reason = (
            "KMP provides predictable linear-time searching "
            "after preprocessing, making it a good default."
        )

    return {
        "algorithm": algorithm,
        "reason": reason,
        "text_length": text_length,
        "pattern_length": pattern_length,
        "distinct_chars": len(counts),
        "distinct_pattern_chars": distinct_pattern_chars,
        "repetition": repetition,
    }


# --------------------------------------------------
# MEASURE PERFORMANCE
# --------------------------------------------------

ALGORITHMS = {
    "Naive": naive_search,
    "KMP": kmp_search,
    "Boyer-Moore": boyer_moore_search,
}


def benchmark(text, pattern):
    results = {}

    for name, function in ALGORITHMS.items():
        start = time.perf_counter()
        positions = function(text, pattern)
        elapsed = (time.perf_counter() - start) * 1000

        results[name] = {
            "positions": positions,
            "time_ms": elapsed,
        }

    return results


# --------------------------------------------------
# STREAMLIT USER INTERFACE
# --------------------------------------------------

st.set_page_config(
    page_title="Hybrid String Matching Selector",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Hybrid String Matching Algorithm Selector")

st.write(
    "Enter a text and a pattern. The system analyzes the input, "
    "selects an algorithm, and shows where the pattern occurs."
)

text_input = st.text_area(
    "Enter the text to search",
    value=(
        "String matching is useful. KMP is efficient. "
        "String matching helps search large text."
    ),
    height=150,
)

pattern_input = st.text_input(
    "Enter the pattern to find",
    value="matching",
)

compare_all = st.checkbox(
    "Compare all three algorithms",
    value=True,
)

if st.button("Analyze and Search", type="primary"):
    if not text_input:
        st.error("Please enter some text.")
    elif not pattern_input:
        st.error("Please enter a search pattern.")
    else:
        info = analyze_input(text_input, pattern_input)
        selected = info["algorithm"]

        st.subheader("Input Analysis")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Text length", info["text_length"])
        col2.metric("Pattern length", info["pattern_length"])
        col3.metric(
            "Distinct text characters", info["distinct_chars"]
        )
        col4.metric(
            "Text repetition",
            f"{info['repetition']:.1%}",
        )

        st.subheader("Selected Algorithm")
        st.success(f"Recommended algorithm: {selected}")
        st.write(info["reason"])

        if compare_all:
            results = benchmark(text_input, pattern_input)
        else:
            start = time.perf_counter()
            positions = ALGORITHMS[selected](
                text_input, pattern_input
            )
            elapsed = (time.perf_counter() - start) * 1000

            results = {
                selected: {
                    "positions": positions,
                    "time_ms": elapsed,
                }
            }

        st.subheader("Search Results")

        selected_result = results[selected]
        positions = selected_result["positions"]

        st.metric("Number of matches", len(positions))

        if positions:
            # Display both zero-based and human-readable positions.
            st.write(
                "Positions (starting from 0):",
                positions,
            )
            st.write(
                "Positions (starting from 1):",
                [p + 1 for p in positions],
            )
        else:
            st.info("No matching pattern was found.")

        st.write(
            f"Selected algorithm time: "
            f"{selected_result['time_ms']:.6f} milliseconds"
        )

        if compare_all:
            st.subheader("Algorithm Performance Comparison")

            for name, result in results.items():
                st.write(
                    f"**{name}:** "
                    f"{len(result['positions'])} matches | "
                    f"{result['time_ms']:.6f} ms"
                )

            st.caption(
                "Small timing differences may be caused by "
                "system load, Python overhead, and input size. "
                "Run multiple trials on larger texts for a "
                "more reliable performance comparison."
            )

        st.subheader("How the Selector Works")
        st.write(
            f"- Text length: {info['text_length']} characters"
        )
        st.write(
            f"- Pattern length: {info['pattern_length']} characters"
        )
        st.write(
            f"- Distinct characters in pattern: "
            f"{info['distinct_pattern_chars']}"
        )
        st.write(
            f"- Fraction of text occupied by its most frequent "
            f"character: {info['repetition']:.1%}"
        )
        st.write(f"- Decision: {selected}")
