CREATE SEQUENCE dbo.MySequence 
  AS BIGINT 
  START WITH 1 
  INCREMENT BY 1;

CREATE TABLE CustomerFeedbackAnalysis (
    UniqueId NVARCHAR(20) NOT NULL 
        CONSTRAINT DF_CustomerFeedbackAnalysis_UniqueId 
        DEFAULT RIGHT(REPLICATE('0', 20) + CAST(NEXT VALUE FOR dbo.MySequence AS VARCHAR(20)), 20),
    FeedbackId  NVARCHAR(50),
    FeedbackText NVARCHAR(MAX),
    Sentiment NVARCHAR(100),
    PositiveScore FLOAT,
    NeutralScore FLOAT,
    NegativeScore FLOAT,
    CONSTRAINT PK_CustomerFeedbackAnalysis PRIMARY KEY (UniqueId)
);