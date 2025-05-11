import React, { useState, useEffect } from "react";
import { Button, Container, Typography, Box, Radio, RadioGroup, FormControlLabel, Checkbox, FormGroup } from "@mui/material";
import { useNavigate } from "react-router-dom";

import singleChoice from "./data/single_choice.json";
import multipleChoice from "./data/multiple_choice.json";

export default function App() {
  const [exam, setExam] = useState(null);
  const [stage, setStage] = useState("initial"); // initial | ready | practicing | result
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const navigate = useNavigate();

  const shuffled = (arr) => [...arr].sort(() => Math.random() - 0.5);

  useEffect(() => {
    const savedExam = localStorage.getItem("exam");
    const savedAnswers = localStorage.getItem("answers");
    if (savedExam) {
      setExam(JSON.parse(savedExam));
      setStage("ready");
    }
    if (savedAnswers) {
      setAnswers(JSON.parse(savedAnswers));
    }
  }, []);

  function generateExam() {
    const single = shuffled(singleChoice).slice(0, 50);
    const multiple = shuffled(multipleChoice).slice(0, 15);
    const full = [...single, ...multiple];
    setExam(full);
    localStorage.setItem("exam", JSON.stringify(full));
    localStorage.removeItem("answers");
    setAnswers({});
    setStage("ready");
  }

  function startPractice() {
    setStage("practicing");
  }

  function handleAnswer(index, selected) {
    const newAnswers = { ...answers, [index]: selected };
    setAnswers(newAnswers);
    localStorage.setItem("answers", JSON.stringify(newAnswers));
  }

  function submitExam() {
    let correct = 0;
    const wrong = [];
    exam.forEach((q, i) => {
      const user = answers[i];
      const ans = q.answer;
      if (Array.isArray(ans)) {
        const sortedUser = [...(user || [])].sort().join("");
        const sortedAns = [...ans].sort().join("");
        if (sortedUser === sortedAns) correct++;
        else wrong.push({ index: i, question: q, yourAnswer: user });
      } else {
        if (user === ans) correct++;
        else wrong.push({ index: i, question: q, yourAnswer: user });
      }
    });
    localStorage.removeItem("exam");
    localStorage.removeItem("answers");
    navigate("/result", { state: { score: correct, total: exam.length, wrong } });
  }

  if (stage === "initial")
    return (
      <Container sx={{ mt: 10, textAlign: "center" }}>
        <Button variant="contained" onClick={generateExam}>Generate</Button>
      </Container>
    );

  if (stage === "ready")
    return (
      <Container sx={{ mt: 10, textAlign: "center" }}>
        <Typography variant="h6">Generated {exam.length} questions</Typography>
        <Button variant="contained" sx={{ mt: 2 }} onClick={startPractice}>Start Practice</Button>
      </Container>
    );

  if (stage === "practicing") {
    const q = exam[current];
    const selected = answers[current] || (Array.isArray(q.answer) ? [] : "");

    return (
      <Container sx={{ mt: 5 }}>
        <Typography variant="h6" gutterBottom>
          Question {current + 1}
        </Typography>
        <Typography variant="body1" gutterBottom>
          {q.question}
        </Typography>
        <Box mt={2}>
          {Array.isArray(q.answer) ? (
            <FormGroup>
              {Object.entries(q.options).map(([key, value]) => (
                <FormControlLabel
                  key={key}
                  control={
                    <Checkbox
                      checked={selected.includes(key)}
                      onChange={() => {
                        const newSelection = selected.includes(key)
                          ? selected.filter((v) => v !== key)
                          : [...selected, key];
                        handleAnswer(current, newSelection);
                      }}
                    />
                  }
                  label={`${key}. ${value}`}
                />
              ))}
            </FormGroup>
          ) : (
            <RadioGroup
              value={selected}
              onChange={(e) => handleAnswer(current, e.target.value)}
            >
              {Object.entries(q.options).map(([key, value]) => (
                <FormControlLabel
                  key={key}
                  value={key}
                  control={<Radio />}
                  label={`${key}. ${value}`}
                />
              ))}
            </RadioGroup>
          )}
        </Box>
        <Box mt={4} display="flex" justifyContent="space-between">
          <Button
            variant="outlined"
            disabled={current === 0}
            onClick={() => setCurrent((c) => Math.max(0, c - 1))}
          >
            Last
          </Button>
          {current < exam.length - 1 ? (
            <Button variant="contained" onClick={() => setCurrent((c) => c + 1)}>Next</Button>
          ) : (
            <Button variant="contained" color="success" onClick={submitExam}>Submit</Button>
          )}
        </Box>
      </Container>
    );
  }

  return null;
}