CREATE TABLE Candidate(
    candidateID INT UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    party VARCHAR(30) UNIQUE NOT NULL,

    PRIMARY KEY (candidateID)
);

CREATE TABLE Vote(
    CPF BIGINT UNIQUE NOT NULL,
    candidateID INT NOT NULL,

    PRIMARY KEY (CPF, candidateID),
    FOREIGN KEY (candidateID) REFERENCES Candidate(CandidateID)
);