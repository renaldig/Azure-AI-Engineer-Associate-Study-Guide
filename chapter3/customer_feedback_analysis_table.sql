CREATE TABLE CustomerFeedbackAnalysis (
  Id INT PRIMARY KEY,
  FeedbackText NVARCHAR(MAX),
  Sentiment NVARCHAR(100),
  Score FLOAT
);
