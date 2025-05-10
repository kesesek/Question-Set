import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Box, Button, Typography, Container } from "@mui/material";

function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const { score, total, wrong } = location.state || {};

  if (!location.state) {
    return (
      <Container sx={{ mt: 6, textAlign: "center" }}>
        <Typography variant="h6" gutterBottom>No records.</Typography>
        <Button variant="contained" onClick={() => navigate("/")}>Back Home</Button>
      </Container>
    );
  }

  return (
    <Container sx={{ mt: 6, maxWidth: "md" }}>
      <Typography variant="h5" gutterBottom>🎯 Result</Typography>
      <Typography variant="body1" gutterBottom>
        You answered {score} out of {total} correctly.
      </Typography>
      <Typography variant="body1" gutterBottom>
        Accuracy: <strong>{((score / total) * 100).toFixed(2)}%</strong>
      </Typography>

      {wrong.length > 0 && (
        <>
          <Typography variant="h6" sx={{ mt: 4 }}>❌ Review mistakes</Typography>
          <Box sx={{ mt: 2 }}>
            {wrong.map((w, idx) => (
              <Box key={idx} sx={{ mb: 3, p: 2, border: '1px solid #ccc', borderRadius: 2 }}>
                <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                  {idx + 1}. {w.question.question}
                </Typography>
                <Box sx={{ ml: 2, mb: 1 }}>
                  {Object.entries(w.question.options).map(([key, value]) => (
                    <Typography key={key} variant="body2">
                      {key}. {value}
                    </Typography>
                  ))}
                </Box>
                <Typography variant="body2" color="error">
                  Your answer: {Array.isArray(w.yourAnswer) ? w.yourAnswer.join(", ") : w.yourAnswer}
                </Typography>
                <Typography variant="body2" color="success.main">
                  Correct answer: {Array.isArray(w.question.answer) ? w.question.answer.join(", ") : w.question.answer}
                </Typography>
              </Box>
            ))}
          </Box>
        </>
      )}

      <Box sx={{ mt: 4, textAlign: "center" }}>
        <Button variant="contained" onClick={() => navigate("/")}>Restart</Button>
      </Box>
    </Container>
  );
}

export default Result;